# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def create(self, vals):
        product = super().create(vals)
        product._create_reordering_rule()
        return product

    def _create_reordering_rule(self, default_locations=False):
        orderpoint_obj = self.env["stock.warehouse.orderpoint"]
        location_obj = self.env["stock.location"]
        warehouses = self.env["stock.warehouse"].search([])
        for warehouse in warehouses:
            cond = [
                ("id", "child_of", [warehouse.lot_stock_id.location_id.id]),
                ("automatic_rule", "=", True),
            ]
            if default_locations:
                cond.append(("id", "in", default_locations.ids))
            locations = location_obj.search(cond)
            for location in locations:
                for product in self:
                    cond = [
                        ("product_id", "=", product.id),
                        ("warehouse_id", "=", warehouse.id),
                        ("location_id", "=", location.id),
                    ]
                    orderpoint = orderpoint_obj.search(cond, limit=1)
                    if not orderpoint:
                        vals = product._catch_values_create_orderpoint(
                            warehouse, location
                        )
                        orderpoint_obj.create(vals)

    def _catch_values_create_orderpoint(self, warehouse, location):
        vals = {
            "product_id": self.id,
            "warehouse_id": warehouse.id,
            "location_id": location.id,
            "product_min_qty": 0,
            "product_max_qty": 0,
        }
        return vals
