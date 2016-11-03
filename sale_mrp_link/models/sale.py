# -*- coding: utf-8 -*-
# © 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, models, fields


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    mrp_production_id = fields.Many2one(
        comodel_name='mrp.production', string='Mrp Production', copy=False)
    product_line_ids = fields.One2many(
        comodel_name='mrp.production.product.line',
        inverse_name='sale_line_id', string='Product line')
    product_uom_qty = fields.Float(
        string='Quantity', compute='_compute_product_price')
    price_unit = fields.Float(
        string='Price Unit', compute='_compute_product_price')

    @api.multi
    @api.depends('mrp_production_id', 'mrp_production_id.product_qty',
                 'mrp_production_id.production_total')
    def _compute_product_price(self):
        for line in self.filtered(lambda x: x.mrp_production_id):
            line.price_unit = (line.mrp_production_id.production_total /
                               line.mrp_production_id.product_qty)
            line.product_uom_qty = line.mrp_production_id.product_qty

    @api.multi
    def need_procurement(self):
        for line in self:
            if line.mrp_production_id:
                return False
            else:
                return super(SaleOrderLine, self).need_procurement()

    @api.multi
    def action_create_mrp(self):
        attribute_list = []
        for attribute_line in self.product_attribute_ids:
            values = {
                'attribute_id': attribute_line.attribute_id.id,
                'value_id': attribute_line.value_id.id,
                'product_tmpl_id': self.product_tmpl_id.id,
                'owner_model': 'mrp.production',
            }
            try:
                values['custom_value'] = attribute_line.custom_value
            except:
                pass
            attribute_list.append(values)
        mrp = self.env['mrp.production'].create({
            'product_tmpl_id': self.product_tmpl_id.id or False,
            'product_id': self.product_id.id or False,
            'product_qty': self.product_uom_qty,
            'product_uom': self.product_tmpl_id.uom_id.id,
            'product_attribute_ids': [(0, 0, x) for x in attribute_list],
            'active': False,
            })
        mrp.write({
            'sale_order': self.order_id.id,
            'sale_line': self.id,
            'partner': self.order_id.partner_id.id,
        })
        self.mrp_production_id = mrp
        self.with_context(sale_line=self.id).action_compute_products()

    @api.multi
    def action_compute_products(self):
        if self.mrp_production_id:
            self.with_context(
                sale_line=self.id).mrp_production_id.action_compute()


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_button_confirm(self):
        res = super(SaleOrder, self).action_button_confirm()
        for mrp in self.mapped('order_line.mrp_production_id'):
            mrp.write({
                'active': True,
                'name': self.env['ir.sequence'].get('mrp.production') or '/',
            })
        return res

    @api.multi
    def action_show_manufacturing_orders(self):
        return {
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'mrp.production',
            'type': 'ir.actions.act_window',
            'search_view_id': self.env.ref(
                'mrp.view_mrp_production_filter').id,
            'domain': "[('sale_order', '=', " + str(self.id) + "),\
                        '|', ('active', '=', True), ('active', '=', False)]",
            'context': self.env.context
            }
