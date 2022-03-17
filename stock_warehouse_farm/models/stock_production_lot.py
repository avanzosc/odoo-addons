# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    operating_number = fields.Char(
        related='location_id.warehouse_id.farm_numexp',
        store=True)
