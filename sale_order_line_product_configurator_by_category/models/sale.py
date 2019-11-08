# Copyright 2019 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _get_last_line(self):
        last_line = self.order_id.order_line.filtered(
            lambda x: x.product_id or x.display_type == 'line_section').sorted(
                "sequence")[-1:]
        return last_line

    @api.multi
    def _get_domain(self):
        self.ensure_one()
        last_line = self._get_last_line()
        restricts = last_line.product_id.restricted_products._ids
        if restricts or not last_line.display_type == 'line_section':
            return restricts
        return False
        # order = self.order_id
        # last_line = order.order_line.sorted("sequence")[-1:]
        # if self.id == last_line.id:
        #     return self.order_id.possible_next_product_ids._ids
        # return []

    @api.onchange("product_id")
    def onchange_order_line(self):
        domain = self._get_domain()
        if domain:
            return {'domain': {'product_id': [
                ('id', 'in', domain)
            ]}}
