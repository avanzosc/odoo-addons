# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class IrModelAccess(models.Model):
    _inherit = "ir.model.access"

    @api.model
    def _restrict_contact_create_unlink_access(self):
        contacts = self.search(
            [
                ("model_id.model", "=", "res.partner"),
                "|",
                ("perm_create", "=", True),
                ("perm_unlink", "=", True),
            ]
        )
        module_access = self.env.ref(
            "res_partner_create_group.access_create_contact", raise_if_not_found=False
        )
        if module_access:
            contacts -= module_access
        contacts.write({"perm_create": False, "perm_unlink": False})

    @api.model
    def init(self):
        self._restrict_contact_create_unlink_access()
