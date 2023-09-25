# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def action_view_move_lines(self):
        context = self.env.context.copy()
        context.update(
            {
                "search_default_groupby_product_id": 2,
                "search_default_from": 1,
                "pivot_measures": ["in_qty", "out_qty", "dif_qty"],
            }
        )
        move_lines = self.env["stock.move.line"].search(
            [("picking_id.partner_id", "in", self.ids)]
        )
        return {
            "name": _("Stock Move Lines"),
            "view_mode": "pivot,tree",
            "res_model": "stock.move.line",
            "domain": [("id", "in", move_lines.ids)],
            "type": "ir.actions.act_window",
            "context": context,
        }
