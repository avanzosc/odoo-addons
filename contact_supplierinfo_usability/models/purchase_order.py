# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    @api.onchange("order_id")
    def onchange_move_id(self):
        domain = self.product_id._search_contact_products(
            "=", self.order_id.partner_id.id
        )
        if domain and len(domain[0][2]) == 1:
            product = self.env["product.product"].search(
                [("product_tmpl_id", "=", domain[0][2][0])]
            )
            self.product_id = product.id
