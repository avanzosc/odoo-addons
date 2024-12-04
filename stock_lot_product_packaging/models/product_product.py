# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    product_package_ids = fields.One2many(
        string="Product Packages",
        comodel_name="product.packaging",
        inverse_name="product_id",
        copy=False,
    )

    def action_create_product_packages(self):
        for product in self:
            for package_type in product.product_tmpl_id.package_type_ids:
                product_package = product._search_product_package(package_type)
                product._search_stock_lot_product_package(product_package)

    def _search_product_package(self, package_type):
        product_packaging_obj = self.env["product.packaging"]
        cond = [("product_id", "=", self.id), ("package_type_id", "=", package_type.id)]
        product_package = product_packaging_obj.search(cond, limit=1)
        if product_package:
            return product_package
        vals = self._get_vals_product_packaging(package_type)
        return product_packaging_obj.create(vals)

    def _get_vals_product_packaging(self, package_type):
        weight_uom = self.env[
            "product.template"
        ]._get_weight_uom_id_from_ir_config_parameter()
        density = (
            self.product_density
            * package_type.packaging_length
            * package_type.width
            * package_type.height
        )
        vals = {
            "product_id": self.id,
            "name": package_type.name,
            "package_type_id": package_type.id,
            "height": package_type.height,
            "width": package_type.width,
            "weight": package_type.base_weight,
            "packaging_length": package_type.packaging_length,
            "max_weight": package_type.max_weight,
            "weight_uom_id": weight_uom.id,
            "qty": density,
        }
        return vals

    def _search_stock_lot_product_package(self, product_package):
        stock_lot_obj = self.env["stock.lot"]
        cond = [
            ("product_id", "=", self.id),
            ("product_packaging_id", "=", product_package.id),
        ]
        stock_lot = stock_lot_obj.search(cond, limit=1)
        if not stock_lot:
            vals = self._get_vals_stock_lot_packaging(product_package)
            stock_lot_obj.create(vals)

    def _get_vals_stock_lot_packaging(self, product_package):
        vals = {"product_id": self.id, "product_packaging_id": product_package.id}
        return vals
