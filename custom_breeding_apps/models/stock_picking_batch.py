# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, fields, models


class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"

    def _compute_eggs_count(self):
        for batch in self:
            batch.egg_count = len(batch.egg_ids)

    egg_ids = fields.One2many(
        string="Eggs",
        comodel_name="stock.move.line",
        inverse_name="batch_id")
    egg_count = fields.Integer(
        '# Eggs', compute='_compute_eggs_count')

    def action_view_eggs(self):
        context = self.env.context.copy()
        context.update({'default_batch_id': self.id})
        return {
            "name": _("Eggs"),
            "view_mode": "tree",
            "res_model": "stock.move.line",
            "domain": [("id", "in", self.egg_ids.ids)],
            "type": "ir.actions.act_window",
            "context": context
        }
