# Copyright 2020 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    product_code = fields.Char(string="Product code")

    @api.onchange("product_id")
    def onchange_product_id(self):
        result = super().onchange_product_id()
        if self.product_id and self.product_id.seller_ids:
            params = {"order_id": self.order_id}
            seller = self.product_id._select_seller(
                partner_id=self.partner_id,
                quantity=self.product_qty,
                date=(self.order_id.date_order and self.order_id.date_order.date()),
                uom_id=self.product_uom,
                params=params,
            )
            name = ""
            if seller and seller.product_name:
                name = seller.product_name
            else:
                name = self.product_id.name
            if not self.product_id.description_purchase:
                self.name = name
            else:
                self.name = "{}\n{}".format(name, self.product_id.description_purchase)
            if seller and seller.product_code:
                self.product_code = seller.product_code
            else:
                if self.product_id.default_code:
                    self.product_code = self.product_id.default_code
        return result
