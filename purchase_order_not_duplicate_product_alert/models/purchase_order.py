# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, models
from odoo.exceptions import ValidationError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def copy(self, default=None):
        for purchase in self:
            for line in purchase.order_line.filtered(
                lambda x: x.product_id and x.product_id.purchase_line_warn == "block"
            ):
                error = _(
                    "You cannot duplicate the purchase order: %(purchase_name)s "
                    "because the product %(product_name)s  is blocked."
                ) % {
                    "purchase_name": purchase.name,
                    "product_name": line.product_id.name,
                }
                raise ValidationError(error)
        return super().copy(default=default)
