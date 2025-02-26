# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class ProductSupplierinfo(models.Model):
    _inherit = "product.supplierinfo"

    @api.model_create_multi
    def create(self, vals_list):
        supplierinfos = super().create(vals_list)
        for supplierinfo in supplierinfos.filtered(lambda x: x.product_brand_id):
            supplierinfo._search_product_brand_supplier_rel()
        return

    def _search_product_brand_supplier_rel(self):
        relation_obj = self.env["product.brand.supplier.relation"]
        cond = [
            ("supplier_id", "=", self.partner_id.id),
            ("product_brand_id", "=", self.product_brand_id.id),
        ]
        relation = relation_obj.search(cond, limit=1)
        if not relation:
            vals = {
                "supplier_id": self.partner_id.id,
                "product_brand_id": self.product_brand_id.id,
            }
            relation = relation_obj.create(vals)
        return relation
