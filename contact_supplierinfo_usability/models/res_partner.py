# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    product_ids = fields.One2many(
        string="Products", comodel_name="product.supplierinfo", inverse_name="name"
    )
    limit_product = fields.Boolean(
        string="Limit the products it provides", default=False
    )
