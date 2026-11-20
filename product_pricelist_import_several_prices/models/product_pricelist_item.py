# Copyright 2026  Ane Gurruchaga - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    rrp_price = fields.Monetary(string="RRP Price")
    distribution_price = fields.Monetary()
