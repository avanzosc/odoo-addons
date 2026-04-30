# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    @api.readonly
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        if (
            "res_partner_search_mode" in self.env.context
            and "show_vat" in self.env.context
            and self.env.context.get("res_partner_search_mode") == "supplier"
            and self.env.context.get("show_vat", False)
        ):
            args += [("is_company", "=", True)]
        return super().name_search(name=name, args=args, operator=operator, limit=limit)
