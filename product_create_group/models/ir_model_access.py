# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class IrModelAccess(models.Model):
    _inherit = "ir.model.access"

    @api.model
    def init(self):
        try:
            group_product_tmpl = self.env.ref(
                "product_create_group.access_create_product_tmpl"
            )
            if group_product_tmpl:
                templates = (
                    self.env["ir.model.access"].search(
                        [
                            ("model_id", "=", "product.template"),
                            "|",
                            ("perm_create", "=", True),
                            ("perm_unlink", "=", True),
                        ]
                    )
                    - group_product_tmpl
                )
        except Exception:
            templates = self.env["ir.model.access"].search(
                [
                    ("model_id", "=", "product.template"),
                    "|",
                    ("perm_create", "=", True),
                    ("perm_unlink", "=", True),
                ]
            )
        for tmpl in templates:
            tmpl.write({"perm_create": False, "perm_unlink": False})
