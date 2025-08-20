# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models

STATE_SELECTION = [
    ("clearance", "Clearance"),
    ("stock", "Stock"),
    ("mto", "Make To Order"),
    ("sample", "Sample"),
    ("discontinued", "Discontinued"),
]


class ProductProduct(models.Model):
    _inherit = "product.product"

    state = fields.Selection(selection=STATE_SELECTION, string="Status")
    shipping_length = fields.Float(string="Length")

    @api.model_create_multi
    def create(self, vals):
        if isinstance(vals, dict):
            vals = self.treatment_shipping_length(vals)
        else:
            for val in vals:
                val = self.treatment_shipping_length(val)
        products = super().create(vals)
        if "no_update_product_state" not in self.env.context:
            for product in products:
                if (
                    product.product_tmpl_id
                    and product.product_tmpl_id.state != product.state
                ):
                    product.product_tmpl_id.with_context(
                        no_update_template_state=True
                    ).write({"state": product.state})
        vals_list = vals if isinstance(vals, list) else [vals]
        has_product_tmpl_id = any("product_tmpl_id" in val for val in vals_list)
        if has_product_tmpl_id:
            for product in products:
                if product.product_tmpl_id.product_variant_count == 1:
                    product.product_tmpl_id.write(
                        {"shipping_length": product.shipping_length}
                    )
        return products

    def write(self, vals):
        result = super().write(vals)
        if (
            "state" in vals
            and vals.get("state", False)
            and "no_update_product_state" not in self.env.context
        ):
            for product in self:
                if product.product_tmpl_id.state != product.state:
                    product.product_tmpl_id.with_context(
                        no_update_template_state=True
                    ).write({"state": product.state})
        if "no_update_template" not in self.env.context and "shipping_length" in vals:
            for product in self:
                if product.product_tmpl_id.product_variant_count == 1:
                    template = product.product_tmpl_id
                    template_vals = {"shipping_length": product.shipping_length}
                    template.with_context(no_update_product=True).write(template_vals)
        return result

    def treatment_shipping_length(self, vals):
        if "product_tmpl_id" in vals and vals.get("product_tmpl_id", False):
            template = self.env["product.template"].browse(vals.get("product_tmpl_id"))
            if template.product_variant_count == 0:
                vals.update({"shipping_length": template.shipping_length})
        return vals
