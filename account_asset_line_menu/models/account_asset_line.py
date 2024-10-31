# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountAssetLine(models.Model):
    _inherit = "account.asset.line"

    profile_id = fields.Many2one(
        comodel_name="account.asset.profile", related="asset_id.profile_id", store=True
    )
    account_analytic_id = fields.Many2one(
        comodel_name="account.analytic.account",
        related="asset_id.account_analytic_id",
        store=True,
    )
