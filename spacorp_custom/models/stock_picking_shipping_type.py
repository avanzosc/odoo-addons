# Copyright 2021 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class StockPickingShippingType(models.Model):
    _name = "stock.picking.shipping.type"
    _description = "Shipping types"

    name = fields.Char(string="Description")
