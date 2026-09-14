# Copyright 2026 Ane Gurruchaga - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models
from odoo.addons import decimal_precision as dp


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    @api.depends("invoice_line_ids.line_weight")
    def _compute_total_weight(self):
        for invoice in self:
            invoice.total_weight = sum(
                invoice.invoice_line_ids.mapped("line_weight")
            )

    total_weight = fields.Float(
        string="Total Weight",
        compute="_compute_total_weight"
    )


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    @api.multi
    @api.depends("quantity", "product_id.weight")
    def _compute_line_weight(self):
        for line in self:
            line.line_weight = line.quantity * line.product_id.weight

    line_weight = fields.Float(
        string="Line Weight",
        compute="_compute_line_weight"
    )
