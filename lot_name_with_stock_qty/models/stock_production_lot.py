# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    def name_get(self):
        result = []
        for lot in self:
            name = u'{} ({})'.format(lot.name, round(lot.product_qty, 2))
            result.append((lot.id, name))
        return result
