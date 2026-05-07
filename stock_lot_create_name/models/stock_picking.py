# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models
from odoo.tools.float_utils import float_compare


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        for picking in self.filtered(
            lambda _picking: (
                _picking.picking_type_id.use_create_lots
                and _picking.picking_type_id.lot_code
            )
        ):
            for move_line in picking.move_line_ids.filtered(
                lambda ml: ml.product_id
                and ml.product_id.tracking == "lot"
                and not ml.lot_name
                and float_compare(
                    ml.qty_done, 0, precision_rounding=ml.product_uom_id.rounding
                )
            ):
                lname = f"{picking.picking_type_id.lot_code}{picking.name[4:]}"
                move_line.write({"lot_name": lname})
        return super().button_validate()
