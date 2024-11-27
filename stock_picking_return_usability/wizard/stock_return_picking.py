# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, models


class StockReturnPicking(models.TransientModel):
    _inherit = "stock.return.picking"

    @api.model
    def _prepare_stock_return_picking_line_vals_from_move(self, stock_move):
        result = super()._prepare_stock_return_picking_line_vals_from_move(stock_move)
        if "quantity" in result and result["quantity"] < 0:
            result["quantity"] = 0
        return result

    def _prepare_move_default_values(self, return_line, new_picking):
        result = super()._prepare_move_default_values(return_line, new_picking)
        if (
            self.picking_id
            and (self.picking_id.picking_type_id)
            and (self.picking_id.picking_type_id.return_picking_type_id)
        ):
            return_type = self.picking_id.picking_type_id.return_picking_type_id
            location = (
                return_type.default_location_src_id
                if return_type.default_location_src_id.usage
                and return_type.default_location_src_id.usage != "view"
                else return_line.move_id.location_dest_id
            )
            location_dest = (
                return_type.default_location_dest_id
                if return_type.default_location_dest_id.usage
                and return_type.default_location_dest_id.usage != "view"
                else return_line.move_id.location_id
            )
            result.update(
                {"location_id": location.id, "location_dest_id": location_dest.id}
            )
        return result

    def _create_returns(self):
        new_picking, picking_type_id = super()._create_returns()
        return_picking = self.env["stock.picking"].browse(new_picking)
        if (
            self.picking_id
            and (self.picking_id.picking_type_id)
            and (self.picking_id.picking_type_id.return_picking_type_id)
        ):
            return_type = self.picking_id.picking_type_id.return_picking_type_id
            location = (
                return_type.default_location_src_id
                if return_type.default_location_src_id.usage
                and return_type.default_location_src_id.usage != "view"
                else self.picking_id.location_dest_id
            )
            location_dest = (
                return_type.default_location_dest_id
                if return_type.default_location_dest_id.usage
                and return_type.default_location_dest_id.usage != "view"
                else self.location_id
            )
            return_picking.write(
                {
                    "location_id": location.id,
                    "location_dest_id": location_dest.id,
                    "origin": _(
                        "{} - Return of {}".format(
                            self.picking_id.origin, self.picking_id.name
                        )
                    ),
                }
            )
        if (
            self.picking_id
            and (self.picking_id.picking_type_id)
            and (self.picking_id.picking_type_id.retun_picking_draft)
        ):
            for move in return_picking.move_ids_without_package:
                move.state = "draft"
        return_picking.do_unreserve()
        for move in return_picking.move_ids_without_package:
            move.with_context(prefetch_fields=False).mapped("move_line_ids").unlink()
            move_line_obj = self.env["stock.move.line"]
            for line in move.origin_returned_move_id.move_line_ids:
                return_move_line = move_line_obj.create(move._prepare_move_line_vals())
                return_move_line.write(
                    {
                        "lot_id": line.lot_id.id,
                        "qty_done": line.qty_done,
                    }
                )
        return new_picking, picking_type_id
