# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, models
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        zero_moves = self.move_ids_without_package.filtered(
            lambda c: c.quantity_done == 0
        )
        for move in zero_moves:
            if move.product_id.tracking != "none" and not move.move_line_ids.filtered(
                lambda ml: ml.lot_id
            ):
                raise UserError(
                    _("You need to supply a Lot/Serial number for product %s")
                    % (move.product_id.display_name)
                )
            move.write(
                {
                    "state": "done",
                    "product_uom_qty": move.quantity_done,
                }
            )
            if not move.move_line_ids:
                self.env["stock.move.line"].create(move._prepare_move_line_vals())
        result = super(StockPicking, self).button_validate()
        return result
