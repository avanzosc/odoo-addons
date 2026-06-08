# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _prepare_procurement_values(self, group_id=False):
        values = super()._prepare_procurement_values(group_id=group_id)
        sale_origin = (
            f"{self.order_id.name} - {self.order_id.client_order_ref}"
            if self.order_id.client_order_ref
            else self.order_id.name
        )
        values["sale_origin"] = sale_origin
        return values
