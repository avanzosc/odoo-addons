# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def button_force_done_detailed_operations(self):
        result = super().button_force_done_detailed_operations()
        for picking in self:
            for line in picking.move_line_ids_without_package:
                if line.move_id and line.move_id.sale_line_id:
                    if line.move_id.sale_line_id.product_packaging:
                        line.product_packaging_id = (
                            line.move_id.sale_line_id.product_packaging.id
                        )
                        line.product_packaging_qty = (
                            line.move_id.sale_line_id.product_packaging_qty
                        )
                    if line.move_id.sale_line_id.palet_id:
                        line.palet_id = line.move_id.sale_line_id.palet_id.id
                        line.palet_qty = line.move_id.sale_line_id.palet_qty
        return result
