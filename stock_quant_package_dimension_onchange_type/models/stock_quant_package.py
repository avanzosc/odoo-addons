# Copyright 2025 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, models


class StockQuantPackage(models.Model):
    _inherit = "stock.quant.package"

    @api.onchange("package_type_id")
    def onchange_package_type_id(self):
        if self.package_type_id:
            self.pack_length = self.package_type_id.packaging_length
            self.width = self.package_type_id.width
            self.height = self.package_type_id.height
            self.pack_weight = self.package_type_id.base_weight
            self.weight_uom_name = self.package_type_id.weight_uom_name
