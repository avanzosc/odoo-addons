# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    financial_account_group_id = fields.Many2one(
        string="Financial Account Group",
        comodel_name="account.group",
        related="general_account_id.group_id",
        store=True,
    )
