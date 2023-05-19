# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class ReturnPicking(models.TransientModel):
    _inherit = 'stock.return.picking'

    def _prepare_move_default_values(self, return_line, new_picking):
        result = super(ReturnPicking, self)._prepare_move_default_values(return_line, new_picking)
        if self.picking_id and self.picking_id.picking_type_id and self.picking_id.picking_type_id.return_picking_type_id:
            result.update({
                "location_id": self.picking_id.picking_type_id.return_picking_type_id.default_location_src_id.id,
                "location_dest_id": self.picking_id.picking_type_id.return_picking_type_id.default_location_dest_id.id})
        return result

    def _create_returns(self):
        new_picking, picking_type_id = super(ReturnPicking, self)._create_returns()
        return_picking = self.env["stock.picking"].browse(new_picking)
        if self.picking_id and self.picking_id.picking_type_id and self.picking_id.picking_type_id.return_picking_type_id:
            return_picking.write({
                "location_id": self.picking_id.picking_type_id.return_picking_type_id.default_location_src_id.id,
                "location_dest_id": self.picking_id.picking_type_id.return_picking_type_id.default_location_dest_id.id})
        if self.picking_id and self.picking_id.picking_type_id and self.picking_id.picking_type_id.retun_picking_draft:
            for move in return_picking.move_ids_without_package:
                move.state = "draft"
        return new_picking, picking_type_id
