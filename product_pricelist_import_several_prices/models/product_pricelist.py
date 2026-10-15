# Copyright 2026 Ane Gurruchaga - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    market_id = fields.Many2one(
        comodel_name="product.pricelist.market",
        string="Market",
    )
