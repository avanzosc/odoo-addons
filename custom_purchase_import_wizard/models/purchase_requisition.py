# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class PurchaseRequisition(models.Model):
    _inherit = "purchase.requisition"

    def name_get(self):
        super().name_get()
        result = []
        for req in self:
            name = req.name
            if req.origin:
                name = "{} - {}".format(name, req.origin)
            result.append((req.id, name))
        return result
