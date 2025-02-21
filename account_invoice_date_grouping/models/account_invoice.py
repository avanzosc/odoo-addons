# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    invoice_month = fields.Char(
        string="Invoice Month",
        compute="_compute_date_fields",
        store=True,
    )
    invoice_year = fields.Char(
        string="Invoice Year",
        compute="_compute_date_fields",
        store=True,
    )
    invoice_quarter = fields.Char(
        string="Invoice Quarter",
        compute="_compute_date_fields",
        store=True,
    )

    @api.depends("date_invoice")
    def _compute_date_fields(self):
        for record in self:
            if record.date_invoice:
                month_number = record.date_invoice.strftime("%m")
                month_name = record.date_invoice.strftime("%B")
                record.invoice_month = f"{month_number} {month_name}"
                record.invoice_year = record.date_invoice.strftime("%Y")
                record.invoice_quarter = "Q" + str(
                    (record.date_invoice.month - 1) // 3 + 1
                )
