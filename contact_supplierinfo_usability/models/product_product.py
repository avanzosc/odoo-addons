# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    product_id_computed = fields.Boolean(
        compute="_compute_auxiliar",
        search="_search_contact_products",
    )

    def _compute_auxiliar(self):
        return True

    def _search_contact_products(self, operator, value):
        partner_id = value
        partner = self.env["res.partner"].search([("id", "=", partner_id)], limit=1)
        if partner and partner.limit_product and partner.product_ids:
            products = []
            for line in partner.product_ids:
                if line.product_tmpl_id.id not in products:
                    products.append(line.product_tmpl_id.id)
            product_id_domain = [("product_tmpl_id", "in", products)]
        else:
            product_id_domain = []
        return product_id_domain
