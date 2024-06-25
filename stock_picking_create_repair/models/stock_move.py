# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StockMove(models.Model):
    _inherit = "stock.move"

    is_repair = fields.Boolean(
        string="It's repair", store=True, copy=False, related="picking_id.is_repair"
    )

    def find_or_create_from_repair(self, picking):
        move = self.search(
            [
                ("picking_id", "=", picking.id),
                ("state", "not in", ["cancel", "done"]),
                ("product_id", "=", self.product_id.id),
            ]
        )
        if move:
            move.write(
                {
                    "product_uom_qty": move.product_uom_qty + self.product_uom_qty,
                }
            )
        else:
            self.copy(
                default={
                    "repair_id": False,
                    "picking_id": picking.id,
                    "location_id": picking.location_id.id,
                    "location_dest_id": picking.location_dest_id.id,
                    "sale_line_id": self.repair_id.sale_line_id.id,
                }
            )
        return move

    # def _action_done(self, cancel_backorder=False):
    #     if self.env.context.get("move_no_to_done"):
    #         return self.env["stock.move"]
    #     else:
    #         return super(StockMove, self)._action_done(
    #             cancel_backorder=cancel_backorder
    #         )

    @api.model
    def create(self, vals):
        if "no_create_move_line" in self.env.context and "move_line_ids" in vals:
            del vals["move_line_ids"]
        if "default_origin_from_devolution" in self.env.context:
            vals["origin"] = self.env.context.get("default_origin_from_devolution")
        move = super().create(vals)
        return move

    def unlink(self):
        for move in self.filtered(
            lambda x: x.state == "draft"
            and x.repair_id
            and x.repair_id.from_repair_picking_out_id
            and x.repair_id.state != "cancel"
            and x.sale_line_id
        ):
            raise ValidationError(
                _(
                    "You cannot delete this movement, because it is associated "
                    "with repair: {}. Go ahead with the out picking, and then "
                    "report the units to be shipped."
                ).format(move.repair_id.name)
            )
        return super().unlink()
