# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class PurchaseRequisitionLine(models.Model):
    _inherit = "purchase.requisition.line"

    def name_get(self):
        super().name_get()
        result = []
        for req in self:
            name = req.product_id.display_name
            if req.origin:
                name = "{} - {}".format(req.origin, name)
            result.append((req.id, name))
        return result
