# Copyright 2021 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    team_id = fields.Many2one(string="Division", comodel_name="crm.team", copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        account_moves = super().create(vals_list)
        for account_move in account_moves:
            if account_move.line_ids:
                teams = account_move.line_ids.mapped("team_id")
                account_move.team_id = teams[0].id if len(set(teams)) == 1 else False
        return account_moves
