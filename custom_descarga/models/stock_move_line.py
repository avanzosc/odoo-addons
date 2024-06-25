# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    @api.onchange("saca_line_id", "qty_done", "product_id", "product_uom_id")
    def onchange_download_unit(self):
        unit = self.env.ref("uom.product_uom_unit")
        if not self.saca_line_id and self.product_uom_id == unit:
            self.download_unit = self.qty_done
