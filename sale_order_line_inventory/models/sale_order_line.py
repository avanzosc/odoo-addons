# Copyright 2020 Alfredo de la  Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def show_product_inventory(self):
        result = self.env.ref("stock.action_view_quants").read()[0]
        result.update(
            {"context": {"search_default_product_tmpl_id": self.product_id.id}}
        )
        return result
