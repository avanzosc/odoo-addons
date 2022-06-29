# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def _prepare_sale_order_data(
            self, name, partner, dest_company, direct_delivery_address):
        result = super(PurchaseOrder, self)._prepare_sale_order_data(
            name, partner, dest_company, direct_delivery_address)
        result["warehouse_id"] = self.saca_line_id.breeding_id.location_id.warehouse_id.id
        result.update({
            "saca_line_id": self.saca_line_id.id})
        return result
