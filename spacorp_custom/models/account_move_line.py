# Copyright 2021 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    team_id = fields.Many2one(string="Division", comodel_name="crm.team", copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)
        for line in lines.filtered(
            lambda x: x.move_id and x.move_id.move_type in ("out_invoice", "out_refund")
        ):
            line.team_id = line.move_id.team_id.id if line.move_id.team_id else False
        return lines
