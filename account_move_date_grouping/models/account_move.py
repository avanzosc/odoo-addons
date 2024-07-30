from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

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

    @api.depends("invoice_date")
    def _compute_date_fields(self):
        for record in self:
            if record.invoice_date:
                month_number = record.invoice_date.strftime("%m")
                month_name = record.invoice_date.strftime("%B")
                record.invoice_month = f"{month_number} {month_name}"
                record.invoice_year = record.invoice_date.strftime("%Y")
                record.invoice_quarter = "Q" + str(
                    (record.invoice_date.month - 1) // 3 + 1
                )
