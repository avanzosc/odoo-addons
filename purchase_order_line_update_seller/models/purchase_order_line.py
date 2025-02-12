# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    update_price_on_tab = fields.Boolean(
        string="Update price on tab",
        default=False,
        copy=False,
    )

    @api.model
    def create(self, values):
        found = False
        if "update_price_on_tab" in values and values.get("update_price_on_tab", False):
            values["update_price_on_tab"] = False
            found = True
        line = super().create(values)
        if found:
            line._treatment_seller_ids()
            pending_lines = line.order_id.order_line.filtered(
                lambda x: x.update_price_on_tab
            )
            if not pending_lines and line.order_id.update_price_on_tab:
                line.order_id.update_price_on_tab = False
        return line

    def write(self, values):
        found = False
        if "update_price_on_tab" in values and values.get("update_price_on_tab", False):
            values["update_price_on_tab"] = False
            found = True
        result = super().write(values)
        if found:
            for line in self:
                line._treatment_seller_ids()
                pending_lines = line.order_id.order_line.filtered(
                    lambda x: x.update_price_on_tab
                )
                if not pending_lines and line.order_id.update_price_on_tab:
                    line.order_id.update_price_on_tab = False
        return result

    def _treatment_seller_ids(self):
        seller = self.env["product.supplierinfo"]
        if self.product_id.seller_ids:
            seller = self.product_id.seller_ids.filtered(
                lambda x: x.partner_id == self.order_id.partner_id and x.min_qty == 0
            )
        if not seller:
            self._create_new_seller_from_purchase_line()
        else:
            if len(seller) > 1:
                seller = min(seller, key=lambda x: x.sequence)
            self._modify_seller_from_purchase_line(seller)

    def _create_new_seller_from_purchase_line(self):
        vals = {
            "product_id": self.product_id.id,
            "product_tmpl_id": self.product_id.product_tmpl_id.id,
            "min_qty": 0,
            "partner_id": self.order_id.partner_id.id,
            "price": self.price_unit,
            "discount": self.discount,
            "date_start": fields.Date.context_today(self),
        }
        self.env["product.supplierinfo"].create(vals)

    def _modify_seller_from_purchase_line(self, seller):
        seller.write(
            {
                "price": self.price_unit,
                "discount": self.discount,
                "date_start": fields.Date.context_today(self),
                "date_end": False,
            }
        )
