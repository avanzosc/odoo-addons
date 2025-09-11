# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class IrModelAccess(models.Model):
    _inherit = "ir.model.access"

    @api.model
    def init(self):
        try:
            group = self.env.ref("res_partner_create_group.access_create_contact")
            if group:
                contacts = (
                    self.env["ir.model.access"].search(
                        [
                            ("model_id", "=", "res.partner"),
                            "|",
                            ("perm_create", "=", True),
                            ("perm_unlink", "=", True),
                        ]
                    )
                    - group
                )
        except Exception:
            contacts = self.env["ir.model.access"].search(
                [
                    ("model_id", "=", "res.partner"),
                    "|",
                    ("perm_create", "=", True),
                    ("perm_unlink", "=", True),
                ]
            )
        for contact in contacts:
            contact.write({"perm_create": False, "perm_unlink": False})
