# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def action_view_distribution(self):
        context = self.env.context.copy()
        return {
            "name": _("Lot/Serial Numbers"),
            "view_mode": "tree,form",
            "res_model": "stock.lot",
            "domain": [
                ("id", "in", self.move_line_ids_without_package.mapped("lot_id").ids)
            ],
            "type": "ir.actions.act_window",
            "context": context,
        }
