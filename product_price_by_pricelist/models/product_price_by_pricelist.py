# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields
from odoo.addons import decimal_precision as dp


class ProductPriceByPricelist(models.Model):
    _name = "product.price.by.pricelist"
    _description = "Product price by pricelist"

    product_id = fields.Many2one(
        string="Product", comodel_name="product.product")
    pricelist_id = fields.Many2one(
        string="Pricelist", comodel_name="product.pricelist")
    price_unit = fields.Float(
        string="Unit Price", digits=dp.get_precision("Product Price"),
        default=0.0)
