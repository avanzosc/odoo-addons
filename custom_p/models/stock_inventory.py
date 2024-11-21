# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, models


class StockInventory(models.Model):
    _inherit = "stock.inventory"

    def action_start(self):
        if not self.location_ids:
            wiz_obj = self.env["stock.inventory.warning.wizard"]
            wiz = wiz_obj.with_context({"active_id": self.id}).create({})
            context = self.env.context.copy()
            return {
                "name": _("Warning"),
                "type": "ir.actions.act_window",
                "res_model": "stock.inventory.warning.wizard",
                "view_type": "form",
                "view_mode": "form",
                "res_id": wiz.id,
                "target": "new",
                "context": context,
            }
        else:
            return super().action_start()
