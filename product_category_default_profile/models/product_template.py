# Copyright 2026 Ane Gurruchaga - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_profile = fields.Boolean()
    profile_product_id = fields.Many2one(
        comodel_name="product.product",
        string="Profile Product",
        domain="[('is_profile', '=', True)]",
    )
    requires_transfer = fields.Boolean()

    @api.model
    def _get_profile_field_names(self):
        return [
            "route_ids",
            "type",
            "is_storable",
            "purchase_ok",
            "sale_ok",
            "property_account_expense_id",
            "property_account_income_id",
            "uom_id",
            "uom_po_id",
            "requires_transfer",
        ]

    @api.model
    def _get_product_default_values(self, product_id):
        product = self.env["product.product"].browse(product_id).exists()
        if not product:
            return {}
        product_template = product.product_tmpl_id
        field_names = self._get_profile_field_names()
        product_template.fetch(field_names)
        values = {
            field_name: product_template._cache[field_name]
            for field_name in field_names
            if field_name in product_template._cache
        }
        return product_template._convert_to_write(values)

    @api.model
    def _get_category_profile_product(self, category_id):
        category = self.env["product.category"].browse(category_id)
        return (
            category.attribute_profile_id.default_profile_product_id
            or category.default_profile_product_id
        )

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            if values.get("is_profile"):
                continue
            profile_product_id = values.get("profile_product_id")
            if not profile_product_id and values.get("categ_id"):
                profile_product = self._get_category_profile_product(values["categ_id"])
                profile_product_id = profile_product.id
                if profile_product_id:
                    values["profile_product_id"] = profile_product_id
            if profile_product_id:
                profile_values = self._get_product_default_values(profile_product_id)
                values.update(profile_values)
        return super().create(vals_list)
