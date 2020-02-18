# Copyright 2019 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    imei = fields.Char(string="Imei")

