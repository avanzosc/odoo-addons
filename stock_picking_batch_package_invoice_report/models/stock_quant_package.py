# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockQuantPackge(models.Model):
    _inherit = "stock.quant.package"

    def get_package_dimensions_to_print(self):
        dimensions = "{} x {} x {}".format(
            self.height, self.width, self.pack_length)
        return dimensions
