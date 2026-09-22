# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class AccountFiscalPositionAccount(models.Model):
    _inherit = "account.fiscal.position.account"

    team_id = fields.Many2one(
        string="Division",
        comodel_name="crm.team",
        copy=False,
    )
