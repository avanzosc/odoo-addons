# Copyright 2026 Ane Gurruchaga - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductPricelistMarket(models.Model):
    _name = "product.pricelist.market"
    _description = "Pricelist Market"
    _order = "name"

    name = fields.Char(required=True)
