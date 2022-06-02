# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class TransportCarrierLinesToInvoice(models.Model):
    _name = "transport.carrier.lines.to.invoice"
    _description = "Transport Carrier Lines to Invoice"

    active = fields.Boolean(default=True, help="Set active to false to hide the Transport Carrier Line without removing it.")
    state = fields.Selection(
        selection=[("to_invoice", "To Invoice"),
                   ("billed", "Billed")],
        string="Status",
        compute='_compute_state',
        copy=False)
    transfer_id = fields.Many2one(
        string='Transfer',
        comodel_name='stock.picking')
    transporter_id = fields.Many2one(
        string='Transporter',
        comodel_name='res.partner')
    product_id = fields.Many2one(
        string='Product',
        comodel_name='product.product')
    product_qty = fields.Float(string='Product Quantity')
    price_unit = fields.Float(string='Price Unit')
    total_price = fields.Float(string='Total Price')
    description = fields.Text(string='Description')
    currency_id = fields.Many2one(
        string='Currency',
        comodel_name='res.currency',
        default=lambda self: self.env.company.currency_id.id)
    supplier_invoice_id = fields.Many2one(
        string='Supplier Invoice',
        comodel_name="account.move")
    date = fields.Date(string='Date')
    shipping_method_id = fields.Many2one(
        string='Shipping Method',
        comodel_name='delivery.carrier')
    product_uom_id = fields.Many2one(
        string='Product UOM',
        comodel_name='uom.uom')
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        related="transfer_id.company_id",
        store=True)

    def _compute_state(self):
        for line in self:
            line.state = 'to_invoice'
            if line.supplier_invoice_id:
                line.state = 'billed'

    def action_invoice(self):
        transporters = []
        for record in self:
            if not record.supplier_invoice_id and record.transporter_id not in transporters:
                transporters.append(record.transporter_id)
                today = fields.Date.today()
                vals = {'partner_id': record.transporter_id.id,
                     'invoice_date': today,
                     'journal_id': self.env['account.journal'].search(
                         [('type', '=', 'purchase')], limit=1).id,
                     'partner_shipping_id': record.transporter_id.id,
                     'invoice_filter_type_domain': 'purchase',
                     'payment_state': 'not_paid',
                     'bank_partner_id': record.transporter_id.id,
                     'move_type': 'in_invoice'}
                account_move = self.env['account.move'].create(vals)
                cond = [
                    ('transporter_id', '=', record.transporter_id.id),
                    ('supplier_invoice_id', '=', False)]
                lines = self.env['transport.carrier.lines.to.invoice'].search(
                    cond)
                for line in lines:
                    if line in self:
                        line.supplier_invoice_id = account_move.id
                        move_line = {'product_id': line.product_id.id,
                                     'partner_id': line.transporter_id.id,
                                     'name': u'{} {}'.format(
                                         line.transfer_id.name, (
                                             line.product_id.name)),
                                     'quantity': line.product_qty,
                                     'product_uom_id': line.product_uom_id.id,
                                     'price_unit': line.price_unit,
                                     'move_id': account_move.id,
                                     'tax_ids': self.env['account.tax'].search(
                                         [('id', '=', 9)]).ids,
                                     }
                        if line.product_id.property_account_expense_id:
                            move_line.update({'account_id': (line.product_id.property_account_expense_id.id)})
                        else:
                            move_line.update({'account_id': line.product_id.categ_id.property_account_expense_categ_id.id})
                        account_move.invoice_line_ids = [(0, 0, move_line)]
