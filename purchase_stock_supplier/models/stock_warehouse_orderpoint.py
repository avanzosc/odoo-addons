# Copyright 2022 AlfredodelaFuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class StockWarehouseOrderpoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"

    @api.onchange("route_id")
    def _onchange_route_id(self):
        result = super()._onchange_route_id()
        if self.product_id and self.route_id:
            self.get_default_supplier()
        return result

    @api.model
    def create(self, vals):
        orderpoints = super().create(vals)
        for orderpoint in orderpoints.filtered(lambda z: not z.supplier_id):
            orderpoint.get_default_supplier()
        return orderpoints

    def get_default_supplier(self):
        for orderpoint in self.filtered(
            lambda x: x.product_id
            and x.route_id
            and x.route_id.rule_ids
            and x.route_id.rule_ids[0].action == "buy"
        ):
            if orderpoint.product_id.seller_ids:
                orderpoint.supplier_id = orderpoint.product_id.seller_ids[0].id
