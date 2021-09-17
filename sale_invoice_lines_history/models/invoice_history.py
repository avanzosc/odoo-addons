# Copyright (c) 2019 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class InvoiceHistory(models.Model):
    _name = "invoice.history"
    _description = "Invoice History"

    name = fields.Char(string="Invoice")
    reference = fields.Char(string="Reference")
    number = fields.Char(string="Number")
    internal_number = fields.Char(string="Internal Number")
    comment = fields.Text(string="Comment")
    amount_tax = fields.Float(string="Taxes", default=0.0)
    amount_total = fields.Float(string="Total", default=0.0)
    amount_untaxed = fields.Float(string="Amount untaxed", default=0.0)
    date_invoice = fields.Date(string="Invoice Date")
    date_due = fields.Date(string="Due Date")
    move_name = fields.Char(string="Move")
    account = fields.Char(string="Account")
    journal = fields.Char(string="Journal")
    partner = fields.Char(string="Partner")
    partner_id = fields.Many2one(comodel_name="res.partner", string="Partner")
    history_line_ids = fields.One2many(
        comodel_name="invoice.move.line.history", inverse_name="invoice_id",
        string="Invoce Lines History"
    )
    type = fields.Char(string="Type")


class InvoiceMoveLineHistory(models.Model):
    _name = "invoice.move.line.history"
    _description = "Invoice Move Line History"

    invoice_id = fields.Many2one(
        comodel_name="invoice.history", string="Invoice Reference",
        required=True)
    partner = fields.Char(string="Partner", related="invoice_id.partner",
                          store=True)
    partner_id = fields.Many2one(
        relation="invoice.history", string="Partner",
        readonly=True, related="invoice_id.partner_id", store=True)
    name = fields.Text(string="Description", required=True)
    product = fields.Char(string="Product")
    quantity = fields.Float(string="Quantity", default=1)
    price_unit = fields.Float(string="Unit Price")
    price_subtotal = fields.Float(string="Price Subtotal")
    discount = fields.Float(string="Discount (%)", default=0.0)
