# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    product_packaging_qty = fields.Float(compute=False, inverse=False)

    @api.onchange("product_qty", "product_uom")
    def _onchange_quantity(self):
        result = super()._onchange_quantity()
        if "warning" in result:
            result = {}
        return result
