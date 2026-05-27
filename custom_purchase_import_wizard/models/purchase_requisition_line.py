# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class PurchaseRequisitionLine(models.Model):
    _inherit = "purchase.requisition.line"

    @api.depends("product_id.display_name", "origin")
    def _compute_display_name(self):
        for req in self:
            name = req.product_id.display_name
            if req.origin:
                name = f"{req.origin} - {name}"
            req.display_name = name
