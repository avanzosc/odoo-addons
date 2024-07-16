# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    num_boxes = fields.Integer(string="Num. Boxes", compute="_compute_num_boxes")

    @api.depends(
        "move_line_ids_without_package", "move_line_ids_without_package.package_qty"
    )
    def _compute_num_boxes(self):
        for picking in self:
            num_boxes = 0
            if picking.move_line_ids_without_package:
                num_boxes = sum(
                    picking.move_line_ids_without_package.mapped("package_qty")
                )
        picking.num_boxes = num_boxes

    def button_num_boxes(self):
        return True
