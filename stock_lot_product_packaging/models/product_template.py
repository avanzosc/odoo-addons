# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    package_type_ids = fields.One2many(
        string="Package types",
        comodel_name="stock.package.type",
        inverse_name="product_tmpl_id",
        copy=False,
    )
    product_density = fields.Float(string="Density", copy=False)

    def action_create_product_packages(self):
        for template in self:
            for product in template.product_variant_ids:
                for package_type in template.package_type_ids:
                    product_package = product._search_product_package(package_type)
                    product._search_stock_lot_product_package(product_package)
