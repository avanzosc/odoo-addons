# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockReturnPicking(models.TransientModel):
    _inherit = "stock.return.picking"

    def _create_returns(self):
        new_picking_id, picking_type_id = super()._create_returns()
        new_picking = self.env["stock.picking"].browse(new_picking_id)
        for line in self.picking_id.move_line_ids.filtered(
            lambda x: x.state == "done" and x.is_repair and x.lot_id and x.sale_line_id
        ):
            for new_line in new_picking.move_line_ids.filtered(
                lambda z: z.product_id == line.product_id and not z.lot_id
            ):
                new_line.lot_id = line.lot_id.id
                new_line._onchange_serial_number()
                break
        if (
            self.picking_id.is_repair
            and self.picking_id.sale_order_id
            and self.picking_id.picking_type_id.code == "outgoing"
        ):
            new_picking.devolution_sale_order_id = self.picking_id.sale_order_id
        return new_picking_id, picking_type_id
