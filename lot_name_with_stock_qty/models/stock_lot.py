# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockLot(models.Model):
    _inherit = "stock.lot"

    def name_get(self):
        result = []
        for lot in self:
            qty = round(lot.product_qty, 2)
            qty = "{:,}".format(qty)
            qty = qty.replace(",", "~").replace(".", ",").replace("~", ".")
            name = "{} ({})".format(lot.name, qty)
            result.append((lot.id, name))
        return result
