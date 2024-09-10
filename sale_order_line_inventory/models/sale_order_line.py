# Copyright 2020 Alfredo de la  Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def show_product_inventory(self):
        self.ensure_one()
        action = self.env.ref("stock.action_view_quants").read()[0]
        action.update(
            {
                "context": {
                    "search_default_product_id": self.product_id.product_tmpl_id.id
                }
            }
        )
        return action
