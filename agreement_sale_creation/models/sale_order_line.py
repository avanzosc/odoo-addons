# Copyright 2025 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _prepare_procurement_values(self, group_id=False):
        self.ensure_one()
        values = super()._prepare_procurement_values(group_id=group_id)
        values.update(
            {
                "agreement_id": self.order_id.agreement_id.id,
            }
        )
        return values
