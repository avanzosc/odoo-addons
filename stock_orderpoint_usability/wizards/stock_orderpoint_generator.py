# Copyright 2021 Daniel Campos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockOrderpointGenerator(models.TransientModel):
    _name = "stock.orderpoint.generator"
    _description = "Wizard to generate stock.warehouse.orderpoints"

    generation_type = fields.Selection(
        selection=[
            ("from_location", "Generate from Location"),
            ("all_0", "Generate 0 Min/Max"),
        ],
        string="Generate Orderpoints",
    )
    location_from = fields.Many2one(
        comodel_name="stock.location",
        string="From Location",
        domain="[('usage','=', 'internal')]",
    )
    location_to = fields.Many2many(
        comodel_name="stock.location",
        string="To Location",
        domain="[('usage','=', 'internal')]",
    )
    update = fields.Boolean(
        help="Check this if you want just update existing orderpoint rules.",
    )

    def _update_orderpoint_rule(self, rule, location):
        """Create/Update location_id with the rule_id provided"""
        orderpoint_obj = self.env["stock.warehouse.orderpoint"]
        rule2update = orderpoint_obj.search(
            [
                ("location_id", "=", location.id),
                ("product_id", "=", rule.product_id.id),
            ]
        )
        if rule2update:
            rule2update.update(
                {
                    "product_min_qty": rule.product_min_qty,
                    "product_max_qty": rule.product_max_qty,
                    "qty_multiple": rule.qty_multiple,
                }
            )
        else:
            rule.copy(
                {
                    "warehouse_id": location.warehouse_id.id,
                    "location_id": location.id,
                }
            )

    def button_generate(self):
        orderpoint_obj = self.env["stock.warehouse.orderpoint"].with_context(
            active_test=False
        )
        product_obj = self.env["product.product"]
        if self.generation_type == "from_location":
            orderpoint_rules = orderpoint_obj.search(
                [("location_id", "=", self.location_from.id)]
            )
            for rule in orderpoint_rules:
                for location in self.location_to:
                    self._update_orderpoint_rule(rule, location)
        elif self.generation_type == "all_0":
            products = product_obj.search([("is_storable", "=", True)])
            for location in self.location_to:
                for product in products:
                    rule_exist = orderpoint_obj.search(
                        [
                            ("location_id", "=", location.id),
                            ("product_id", "=", product.id),
                        ]
                    )
                    if rule_exist:
                        continue
                    rule_data = {
                        "warehouse_id": location.warehouse_id.id,
                        "location_id": location.id,
                        "product_id": product.id,
                    }
                    try:
                        orderpoint_obj.create(rule_data)
                    except Exception:
                        continue
