# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def action_view_move_line_report(self):
        context = self.env.context.copy()
        context.update(
            {
                "search_default_groupby_product": 2,
                "search_default_from": 1,
                "pivot_measures": ["entry_qty", "output_qty", "qty_done"],
            }
        )
        move_lines = self.env["stock.move.line.report"].search(
            [("partner_id", "in", self.ids)]
        )
        cron = self.env.ref("custom_move_line_report.refresh_materialized_view")
        if cron:
            cron.method_direct_trigger()
        return {
            "name": _("Stock Move Lines Report"),
            "view_mode": "pivot,tree",
            "res_model": "stock.move.line.report",
            "domain": [("id", "in", move_lines.ids)],
            "type": "ir.actions.act_window",
            "context": context,
        }
