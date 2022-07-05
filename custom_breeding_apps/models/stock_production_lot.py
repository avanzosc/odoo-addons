# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"
    _order = "name desc"

    def name_get(self):
        result = []
        for lot in self:
            name = u'{} ({})'.format(lot.name, lot.product_qty)
            result.append((lot.id, name))
        return result
