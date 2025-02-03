# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def create_sale_info_section(self):
        for sale in self:
            my_name = _("Order: %(order)s, Date: %(date)s") % {
                "order": sale.name,
                "date": sale.date_order.date(),
            }
            line = sale.order_line.filtered(lambda x: x.name == my_name)
            if not line:
                line = self.env["sale.order.line"].create(
                    sale._get_values_sale_info_section(my_name)
                )
                line._compute_invoice_status()
                self._cr.commit()

    def _get_values_sale_info_section(self, my_name):
        vals = {
            "name": my_name,
            "order_id": self.id,
            "sequence": 1,
            "display_type": "line_section",
        }
        return vals
