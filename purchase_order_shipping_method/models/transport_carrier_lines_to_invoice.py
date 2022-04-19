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

    def _compute_state(self):
        for line in self:
            line.state = 'to_invoice'
            if line.supplier_invoice_id:
                line.state = 'billed'
