# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from odoo.tools import SQL


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    current_user_id = fields.Many2one(
        comodel_name="res.users", string="Current Salesperson", readonly=True
    )

    @api.model
    def _select(self):
        return SQL("%s, move.current_user_id as current_user_id", super()._select())
