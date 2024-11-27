# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    date = fields.Date(string="Accounting Date", readonly=True)

    @api.model
    def _select(self):
        return super()._select() + ", move.date"
