# Copyright 2020 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models, exceptions, _
from odoo.addons import decimal_precision as dp


class StockMove(models.Model):
    _inherit = "stock.move"

    categ_id = fields.Many2one(comodel_name="product.category",
                               related="product_id.categ_id", store=True)
    product_brand_id = fields.Many2one(comodel_name="product.brand",
                                       related="product_id.product_brand_id",
                                       store=True)
