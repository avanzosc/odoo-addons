# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    country_id = fields.Many2one(
        string="Origin", comodel_name="res.country")
    ref = fields.Char(
        string="Global Gap")
