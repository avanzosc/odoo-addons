# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api


class StockSaleServiceLine(models.Model):

    _name = 'stock.sale.service.line'

    picking_id = fields.Many2one(comodel_name='stock.picking',
                                 string='Picking')
    sale_line_id = fields.Many2one(comodel_name='sale.order.line',
                                   string='Sale line')
    in_picking = fields.Boolean(string='In Picking')
    product_qty = fields.Float(related='sale_line_id.product_uom_qty',
                               string='Quantity')
    price_unit = fields.Float(related='sale_line_id.price_unit',
                              string='Unit Price')
    discount = fields.Float(related='sale_line_id.discount', string='Discount')
    price_subtotal = fields.Float(related='sale_line_id.price_subtotal',
                                  string='Subtotal')


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    @api.multi
    def get_service_lines(self, sale=False):
        service_lines = []
        if sale:
            for line in sale.order_line.filtered(lambda x: x.product_id.type ==
                                                 'service'):
                service_lines += [(0, 0, {'in_picking': True,
                                          'sale_line_id': line.id})]
        self.write({'sale_service_lines': service_lines})

    sale_service_lines = fields.One2many(
        comodel_name='stock.sale.service.line', inverse_name='picking_id',
        string='Sale Service Lines')
    amount_untaxed = fields.Float(compute='_amount_all')
    amount_tax = fields.Float(compute='_amount_all')
    amount_total = fields.Float(compute='_amount_all')

    @api.model
    def _create_backorder(self, picking, backorder_moves=None):
        if not backorder_moves:
            backorder_moves = []
        res = super(StockPicking, self)._create_backorder(
            picking, backorder_moves=backorder_moves or [])
        if res:
            backorder_service_lines = picking.sale_service_lines.filtered(
                lambda x: not x.in_picking)
            backorder_service_lines.write({'picking_id': res,
                                           'in_picking': True})
        return res

    @api.multi
    @api.depends('move_lines', 'move_lines.product_qty',
                 'move_lines.product_uos_qty', 'sale_service_lines')
    def _amount_all(self):
        for picking in self:
            picking.amount_untaxed = 0.0
            picking.amount_total = 0.0
            val2 = val1 = val = 0.0
            for line in picking.move_lines.filtered(
                    lambda x: x.procurement_id.sale_line_id):
                sale_line = line.procurement_id.sale_line_id
                cur = sale_line.order_id.pricelist_id.currency_id
                price = sale_line.price_unit * (
                    1 - (sale_line.discount or 0.0) / 100.0)
                taxes = sale_line.tax_id.compute_all(
                    price, line.product_qty,
                    sale_line.order_id.partner_invoice_id.id,
                    line.product_id, sale_line.order_id.partner_id)
                val1 += cur.round(taxes['total'])
                val += cur.round(taxes['total_included'])
                for tax in taxes['taxes']:
                    val2 += tax.get('amount', 0.0)
            for service_line in picking.sale_service_lines:
                sale_line = service_line.sale_line_id
                cur = sale_line.order_id.pricelist_id.currency_id
                price = sale_line.price_unit * (
                    1 - (sale_line.discount or 0.0) / 100.0)
                taxes = sale_line.tax_id.compute_all(
                    price, sale_line.product_uom_qty,
                    sale_line.order_id.partner_invoice_id.id,
                    sale_line.product_id, sale_line.order_id.partner_id)
                val1 += cur.round(taxes['total'])
                val += cur.round(taxes['total_included'])
                for tax in taxes['taxes']:
                    val2 += tax.get('amount', 0.0)
            picking.amount_untaxed = val1
            picking.amount_tax = val2
            picking.amount_total = val

    @api.multi
    def compute(self, picking):
        if not picking.sale_id:
            return {}
        tax_grouped = {}
        order = picking.sale_id
        currency = order.currency_id.with_context(
            date=order.date_order or fields.Date.context_today(order))
        for move in picking.move_lines:
            sale_line = move.procurement_id.sale_line_id
            price = sale_line.price_unit * (1 - (sale_line.discount or 0.0) /
                                            100)
            taxes = sale_line.tax_id.compute_all(
                price, move.product_qty, move.product_id,
                picking.partner_id)['taxes']
            for tax in taxes:
                val = {
                    'picking': picking.id,
                    'name': tax['name'],
                    'amount': tax['amount'],
                    'base': currency.round(tax['price_unit'] *
                                           move.product_qty),
                    'sequence': tax['sequence'],
                    'base_code_id': tax['base_code_id'],
                    'tax_code_id': tax['tax_code_id'],
                }
                key = (val['tax_code_id'], val['base_code_id'])
                if key not in tax_grouped:
                    tax_grouped[key] = val
                else:
                    tax_grouped[key]['base'] += val['base']
                    tax_grouped[key]['amount'] += val['amount']
        for service_line in picking.sale_service_lines:
            sale_line = service_line.sale_line_id
            price = sale_line.price_unit * (1 - (sale_line.discount or 0.0) /
                                            100)
            taxes = sale_line.tax_id.compute_all(
                price, sale_line.product_uom_qty, sale_line.product_id,
                picking.partner_id)['taxes']
            for tax in taxes:
                val = {
                    'picking': picking.id,
                    'name': tax['name'],
                    'amount': tax['amount'],
                    'base': currency.round(tax['price_unit'] *
                                           sale_line.product_uom_qty),
                    'sequence': tax['sequence'],
                    'base_code_id': tax['base_code_id'],
                    'tax_code_id': tax['tax_code_id'],
                }
                key = (val['tax_code_id'], val['base_code_id'])
                if key not in tax_grouped:
                    tax_grouped[key] = val
                else:
                    tax_grouped[key]['base'] += val['base']
                    tax_grouped[key]['amount'] += val['amount']
        for t in tax_grouped.values():
            t['base'] = currency.round(t['base'])
            t['amount'] = currency.round(t['amount'])
        return tax_grouped


class StockMove(models.Model):

    _inherit = 'stock.move'

    @api.model
    def _create_invoice_line_from_vals(self, move, invoice_line_vals):
        invoice_line_obj = self.env['account.invoice.line']
        for line in move.picking_id.sale_service_lines.filtered(
                lambda x: not x.sale_line_id.invoiced):
            line_ids = line.sale_line_id.invoice_line_create()
            lines = invoice_line_obj.browse(line_ids)
            lines.write({'invoice_id': invoice_line_vals.get('invoice_id')})
        return super(StockMove, self.with_context(not_create_service=True)
                     )._create_invoice_line_from_vals(move, invoice_line_vals)
