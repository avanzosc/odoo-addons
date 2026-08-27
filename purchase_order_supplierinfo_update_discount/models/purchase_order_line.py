# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    def write(self, vals):
        res = super().write(vals)
        if vals.get("discount"):
            self.update_supplierinfo_price()
        return res

    def _update_supplierinfo(self, seller):
        self.ensure_one()
        result = super()._update_supplierinfo(seller)
        seller.discount = self.discount
        return result
