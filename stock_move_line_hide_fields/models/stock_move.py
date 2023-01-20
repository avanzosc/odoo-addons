# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockMove(models.Model):
    _inherit = 'stock.move'

    def action_show_details(self):
        self.ensure_one()
        result = super(StockMove, self).action_show_details()
        if self.picking_type_id.code == "incoming":
            result["context"]["show_destination_location"] = False
            result["context"]["show_qty_done"] = False
            result["context"]["show_product_uom"] = False
        return result
