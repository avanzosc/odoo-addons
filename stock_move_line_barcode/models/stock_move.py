# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class StockMove(models.Model):
    _inherit = "stock.move"

    def action_show_details(self):
        result = super(StockMove, self).action_show_details()
        if self.product_id.tracking and self.product_id.tracking == "serial":
            result["context"]["default_for_barcode"] = True
        return result
