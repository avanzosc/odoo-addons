# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockRule(models.Model):
    _inherit = "stock.rule"

    def _make_po_get_domain(self, company_id, values, partner):
        domain = super()._make_po_get_domain(company_id, values, partner)
        if "sale_origin" in self.env.context:
            domain += (("origin", "=", self.env.context.get("sale_origin")),)
        if (
            "from_orderpoint" in self.env.context
            and self.env.context.get("from_orderpoint", False)
            and "orderpoint_id" in values
            and values.get("orderpoint_id", False)
        ):
            domain += (("origin", "=", "New reordering rule"),)
        return domain
