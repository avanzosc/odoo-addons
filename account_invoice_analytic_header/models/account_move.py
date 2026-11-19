# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    analytic_account_id = fields.Many2one(
        comodel_name="account.analytic.account",
        string="Analytic Account",
        help="Analytic account applied by default to invoice lines.",
    )

    @api.onchange("analytic_account_id")
    def _onchange_analytic_account_id(self):
        for move in self:
            for line in move.invoice_line_ids:
                line.analytic_account_id = move.analytic_account_id
