# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class AccountAccount(models.Model):
    _inherit = "account.account"

    analytic_template_ids = fields.One2many(
        string="Analytic Distribution",
        comodel_name="account.analytic.template",
        inverse_name="account_id",
    )
