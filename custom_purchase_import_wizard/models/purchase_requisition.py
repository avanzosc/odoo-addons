# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class PurchaseRequisition(models.Model):
    _inherit = "purchase.requisition"

    @api.depends("name", "reference")
    def _compute_display_name(self):
        for req in self:
            name = req.name
            if req.reference:
                name = f"{name} - {req.reference}"
            req.display_name = name
