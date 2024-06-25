# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def create_automatic_packages(self):
        for picking in self:
            move_lines = picking.move_line_ids_without_package.filtered(
                lambda x: not x.result_package_id and x.product_packaging
            )
            if move_lines:
                pack_vals = {"picking_id": picking.id}
                count = picking.qty_packages
                for line in move_lines:
                    if line.product_packaging:
                        pack_vals["packaging_id"] = line.product_packaging.id
                    count += 1
                    name = "{} {} {}{}".format(picking.name, "-", "00", count)
                    pack_vals["name"] = name
                    package = self.env["stock.quant.package"].create(pack_vals)
                    line.result_package_id = package.id
                if count != picking.qty_packages:
                    picking.qty_packages = count
