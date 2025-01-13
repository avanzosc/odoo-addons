# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import SUPERUSER_ID, api


@api.model
def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    contacts = env["ir.model.access"].search(
        [
            ("model_id", "=", "res.partner"),
            "|",
            ("perm_create", "=", True),
            ("perm_unlink", "=", True),
        ]
    ) - env.ref("res_partner_create_group.access_create_contact")
    for contact in contacts:
        contact.write({"perm_create": False, "perm_unlink": False})
