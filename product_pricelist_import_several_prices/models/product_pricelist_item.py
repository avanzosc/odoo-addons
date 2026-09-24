# Copyright 2026  Ane Gurruchaga - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    pvp_price = fields.Float(string="PVP")
    distribution_price = fields.Float()
