# Copyright (c) 2019 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# Copyright (c) 2026 Eñaut Alberdi - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class InvoiceHistory(models.Model):
    _name = "invoice.history"
    _description = "Invoice History"

    name = fields.Char(string="Invoice")
    reference = fields.Char()
    number = fields.Char()
    internal_number = fields.Char()
    comment = fields.Text()
    amount_tax = fields.Float(string="Taxes", default=0.0)
    amount_total = fields.Float(string="Total", default=0.0)
    amount_untaxed = fields.Float(string="Amount untaxed", default=0.0)
    date_invoice = fields.Date(string="Invoice Date")
    date_due = fields.Date(string="Due Date")
    move_name = fields.Char(string="Move ")
    account = fields.Char()
    journal = fields.Char()
    partner = fields.Char()
    partner_id = fields.Many2one(comodel_name="res.partner")
    history_lines = fields.One2many(
        comodel_name="invoice.move.line.history",
        inverse_name="invoice_id",
        string="Invoce Lines History",
    )
    type = fields.Char()


class InvoiceMoveLineHistory(models.Model):
    _name = "invoice.move.line.history"
    _description = "Invoice Move Line History"

    invoice_id = fields.Many2one(
        comodel_name="invoice.history", string="Invoice Reference", required=True
    )
    partner = fields.Char(compute="_compute_partner", store=True, readonly=False)
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        readonly=True,
        related="invoice_id.partner_id",
        store=True,
    )
    name = fields.Text(string="Description", required=True)
    product = fields.Char()
    quantity = fields.Float(default=1)
    price_unit = fields.Float(string="Unit Price")
    price_subtotal = fields.Float()
    discount = fields.Float(string="Discount (%)", default=0.0)

    @api.depends("invoice_id.partner", "invoice_id.partner_id.name")
    def _compute_partner(self):
        for line in self:
            line.partner = (
                line.invoice_id.partner or line.invoice_id.partner_id.name or False
            )
