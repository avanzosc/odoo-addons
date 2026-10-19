# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class ThermoformedCostCommon(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls.company.write(
            {
                "margin_purchase": 10.0,
                "value_added_margin": 20.0,
                "costs_operator": 25.0,
                "costs_mechanic": 30.0,
            }
        )

        cls.product_category = cls.env["product.category"].create(
            {"name": "Test Category"}
        )
        cls.material_product = cls.env["product.template"].create(
            {
                "name": "Test Material",
                "density": 0.92,
                "list_price": 1.5,
                "categ_id": cls.product_category.id,
            }
        )
        cls.box_product = cls.env["product.template"].create(
            {
                "name": "Test Box",
                "list_price": 0.50,
                "categ_id": cls.product_category.id,
            }
        )
        cls.pallet_product = cls.env["product.template"].create(
            {
                "name": "Test Pallet",
                "list_price": 12.0,
                "categ_id": cls.product_category.id,
            }
        )

        cls.workcenter = cls.env["mrp.workcenter"].create(
            {
                "name": "Test Workcenter",
                "costs_hour": 50.0,
                "company_id": cls.company.id,
            }
        )

        cls.frame = cls.env["frame"].create(
            {
                "name": "Frame 01",
                "workcenter_id": cls.workcenter.id,
                "width": 500.0,
                "step": 400.0,
                "description": "Test frame",
            }
        )

        cls.thermoformed_cost_vals = {
            "product_id": cls.material_product.id,
            "variant_id": cls.material_product.product_variant_id.id,
            "workcenter_id": cls.workcenter.id,
            "frame_id": cls.frame.id,
            "width": 500.0,
            "step": 400.0,
            "thickness": 0.8,
            "density": 0.92,
            "serie": 10000,
            "figure": 6,
            "plate_hour": 50,
            "adjustment_plates": 100,
            "waste_percentage": 3.0,
            "material_cost": 1.5,
            "workcenter_cost": 50.0,
            "operator_cost": 25.0,
            "mechanic_cost": 30.0,
            "operator": 1.0,
            "assembly": 2.0,
            "box_id": cls.box_product.id,
            "box_quantity": 50,
            "pallet_id": cls.pallet_product.id,
            "box_pallet": 16,
            "box_cost": 0.50,
            "pallet_cost": 12.0,
            "pallet_transport_cost": 40.0,
            "margin_purchase": 10.0,
            "value_added_margin": 20.0,
            "commission": 1.0,
            "annual_amount": 10000,
            "unit_retail_price": 5.0,
        }

        dp_model = cls.env["decimal.precision"]
        cls.dp_product_price = dp_model.precision_get("Product Price")
        cls.dp_stock_weight = dp_model.precision_get("Stock Weight")
        cls.dp_discount = dp_model.precision_get("Discount")
        cls.dp_price_unit = dp_model.precision_get("Price Unit")

    def _create_thermoformed_cost(self, **kwargs):
        vals = dict(self.thermoformed_cost_vals, **kwargs)
        return self.env["thermoformed.cost"].create(vals)
