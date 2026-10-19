# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, models
from odoo.exceptions import UserError


class StockQuant(models.Model):
    _inherit = "stock.quant"

    def action_stock_quant_relocate(self):
        if (
            len(self.company_id) > 1
            or any(not q.company_id.id for q in self)
            or any(q <= 0 for q in self.mapped("quantity"))
        ):
            raise UserError(
                _(
                    "You can only move positive quantities stored in locations "
                    "used by a single company per relocation."
                )
            )
        context = {
            "default_quant_ids": self.ids,
            "default_lot_id": self.env.context.get("default_lot_id", False),
            "single_product": self.env.context.get("single_product", False),
        }
        return {
            "res_model": "stock.quant.relocate",
            "views": [[False, "form"]],
            "target": "new",
            "type": "ir.actions.act_window",
            "context": context,
        }

    def action_clear_inventory_quantity(self):
        self.inventory_quantity = 0
        self.inventory_diff_quantity = 0
        self.inventory_quantity_set = False
        self.user_id = False

    def move_quants(
        self, location_dest_id=False, package_dest_id=False, message=False, unpack=False
    ):
        message = message or _("Quantity Relocated")
        move_vals = []
        for quant in self:
            move_vals.append(
                quant.with_context(inventory_name=message)._get_inventory_move_values(
                    quant.quantity,
                    quant.location_id,
                    location_dest_id or quant.location_id,
                )
            )
        moves = self.env["stock.move"].create(move_vals)
        moves._action_done()
