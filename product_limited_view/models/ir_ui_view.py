# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class Model(models.AbstractModel):
    _inherit = "base"

    def _get_view(self, view_id=None, view_type="form", **options):
        if self == self.env["product.product"]:
            if self.env.user.has_group(
                "product_limited_view.group_product_limited_view"
            ):
                if view_type == "form":
                    view_id = self.env.ref(
                        "product_limited_view." "product_product_base_minimal_form"
                    ).id
                elif view_type == "tree":
                    view_id = self.env.ref(
                        "product_limited_view." "product_product_minimal_tree"
                    ).id

        if self == self.env["product.template"]:
            if self.env.user.has_group(
                "product_limited_view.group_product_limited_view"
            ):
                if view_type == "form":
                    view_id = self.env.ref(
                        "product_limited_view." "product_template_base_minimal_form"
                    ).id
                elif view_type == "tree":
                    view_id = self.env.ref(
                        "product_limited_view." "product_template_minimal_tree"
                    ).id
        return super()._get_view(view_id=view_id, view_type=view_type, **options)
