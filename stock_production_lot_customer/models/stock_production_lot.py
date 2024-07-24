# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    customer_id = fields.Many2one(string="Customer", comodel_name="res.partner")
