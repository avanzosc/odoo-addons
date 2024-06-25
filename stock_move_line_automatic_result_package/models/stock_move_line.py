# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)
        for line in lines:
            vals = {
                "container": line.move_id.container,
                "package_qty": line.move_id.package_qty,
            }
            if line.move_id.product_packaging:
                vals["product_packaging"] = line.move_id.product_packaging.id
            if vals:
                line.write(vals)
        return lines
