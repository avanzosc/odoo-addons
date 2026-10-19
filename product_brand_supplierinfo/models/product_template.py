# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    brand_product_count = fields.Integer(
        string="Brand Product Counter", compute="_compute_brand_product_count"
    )

    def _compute_brand_product_count(self):
        for template in self:
            brand_products = template._search_brand_products()
            template.brand_product_count = len(brand_products)

    def action_view_brand_products(self):
        self.ensure_one()
        brand_products = self._search_brand_products()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "product_brand_supplierinfo.brand_product_action"
        )
        action["domain"] = [("id", "in", brand_products.ids)]
        return action

    def _search_brand_products(self):
        cond = [("product_tmpl_id", "=", self.id)]
        return self.env["brand.product"].search(cond)
