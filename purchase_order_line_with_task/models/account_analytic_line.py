# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, models


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    @api.model
    def create(self, vals):
        if vals.get("move_id", False):
            line = self.env["account.move.line"].browse(vals.get('move_id'))
            if line.task_id:
                vals.update({
                    "task_id": line.task_id.id,
                })
        return super(AccountAnalyticLine, self).create(vals)
