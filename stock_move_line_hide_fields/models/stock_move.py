# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def action_show_details(self):
        self.ensure_one()
        result = super(StockMove, self).action_show_details()
        if (
            self.picking_type_id.code == "incoming"
            and self.product_id.tracking
            and self.product_id.tracking == "serial"
        ):
            result["context"]["no_show_qty_done"] = True
            result["context"]["no_show_product_uom"] = True
        return result
