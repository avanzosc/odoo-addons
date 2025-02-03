# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def _add_supplier_to_product(self):
        result = super(PurchaseOrder, self)._add_supplier_to_product()
        self._update_supplier_info_to_product()
        return result

    def _update_supplier_info_to_product(self):
        for line in self.order_line:
            partner = (
                self.partner_id
                if not self.partner_id.parent_id
                else self.partner_id.parent_id
            )
            seller = self._find_seller_to_update_suppliernfo_to_product(line, partner)
            if seller:
                vals = self._catch_values_to_update_seller_in_product(line, seller)
                seller.write(vals)

    def _catch_values_to_update_seller_in_product(self, line, seller):
        vals = {}
        if seller.price != line.price_unit:
            vals["price"] = line.price_unit
        if seller.discount != line.discount:
            vals["discount"] = line.discount
        return vals

    def _find_seller_to_update_suppliernfo_to_product(self, line, partner):
        seller = line.product_id.seller_ids.filtered(
            lambda x: x.name == partner
            and (x.price != line.price_unit or x.discount != line.discount)
        )
        return seller
