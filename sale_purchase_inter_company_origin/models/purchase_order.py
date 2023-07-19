# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def _prepare_sale_order_data(self, name, partner, company,
                                 direct_delivery_address):
        values = super(PurchaseOrder, self)._prepare_sale_order_data(
            name, partner, company, direct_delivery_address)
        if self.origin:
            values["origin"] = self.origin
        return values
