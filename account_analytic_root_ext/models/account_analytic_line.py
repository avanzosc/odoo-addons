# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    root_analytic_account_id = fields.Many2one(
        string="Top Parent Analytic Account",
        comodel_name="account.analytic.account",
        related="account_id.root_analytic_account_id",
        store=True,
    )
