# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import SUPERUSER_ID, api


@api.model
def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    product_tmpls = env["ir.model.access"].search(
        [
            ("model_id", "=", "product.template"),
            "|",
            ("perm_create", "=", True),
            ("perm_unlink", "=", True),
        ]
    ) - env.ref("product_create_group.access_create_product_tmpl")
    for tmpl in product_tmpls:
        tmpl.write({"perm_create": False, "perm_unlink": False})
