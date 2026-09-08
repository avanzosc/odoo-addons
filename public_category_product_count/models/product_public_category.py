# Copyright 2025 Eñaut Alberdi Korta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductPublicCategory(models.Model):
    _inherit = "product.public.category"

    product_count = fields.Integer(
        string="Number of Products",
        compute="_compute_product_count",
        store=False,
    )

    @api.depends("product_tmpl_ids")
    def _compute_product_count(self):
        for category in self:
            category.product_count = len(category.product_tmpl_ids)

    def action_open_category_products(self):
        self.ensure_one()

        action = self.env["ir.actions.act_window"]._for_xml_id(
            "product.product_template_action"
        )
        action["name"] = self.env._("Products in %s", self.display_name)
        action["domain"] = [("public_categ_ids", "in", self.ids)]
        action["context"] = {"default_public_categ_ids": [self.id]}
        return action
