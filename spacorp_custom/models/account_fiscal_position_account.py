# Copyright 2021 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class AccountFiscalPositionAccount(models.Model):
    _inherit = "account.fiscal.position.account"
    _order = "account_src_id"

    team_id = fields.Many2one(
        string="Division",
        comodel_name="crm.team",
        copy=False,
    )
