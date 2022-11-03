# Copyright 2022 AlfredodelaFuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, api


class StockWarehouseOrderpoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"

    @api.model
    def create(self, vals):
        orderpoint = super(StockWarehouseOrderpoint, self).create(vals)
        if not orderpoint.supplier_id:
            orderpoint.get_default_supplier()
        return orderpoint

    def get_default_supplier(self):
        for orderpoint in self.filtered(lambda x: x.product_id):
            if orderpoint.product_id.seller_ids:
                orderpoint.supplier_id = orderpoint.product_id.seller_ids[0].id
