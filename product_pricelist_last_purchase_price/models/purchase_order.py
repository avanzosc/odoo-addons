# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, models
from odoo.exceptions import ValidationError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def _find_seller_to_update_suppliernfo_to_product(self, line, partner):
        seller = super(
            PurchaseOrder, self
        )._find_seller_to_update_suppliernfo_to_product(line, partner)
        if len(seller) > 1:
            message = _(
                "The product: %(product)s has been repeated more than "
                "once by supplier: %(supplier)s."
            ) % {"product": line.product_id.name, "supplier": partner.name}
            raise ValidationError(message)
        if seller and seller.not_update_price_from_order:
            seller = False
        return seller
