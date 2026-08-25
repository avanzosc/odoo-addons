# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import psycopg2

from odoo.exceptions import ValidationError
from odoo.tests import tagged
from odoo.tools import float_round

from .common import ThermoformedCostCommon


@tagged("post_install", "-at_install")
class TestThermoformedCostCreate(ThermoformedCostCommon):
    def test_create_auto_sequence(self):
        cost1 = self._create_thermoformed_cost()
        cost2 = self._create_thermoformed_cost()
        self.assertNotEqual(cost1.name, cost2.name)
        self.assertTrue(cost1.name.startswith("THR"))

    def test_create_custom_name(self):
        cost = self._create_thermoformed_cost(name="CUSTOM-001")
        self.assertEqual(cost.name, "CUSTOM-001")

    def test_create_default_state(self):
        cost = self._create_thermoformed_cost()
        self.assertEqual(cost.state, "draft")

    def test_create_density_from_product(self):
        cost = self.env["thermoformed.cost"].create(
            {
                "product_id": self.material_product.id,
                "width": 500.0,
                "step": 400.0,
                "thickness": 0.8,
            }
        )
        self.assertAlmostEqual(cost.density, self.material_product.density, places=4)

    def test_create_density_explicit_not_overridden(self):
        cost = self.env["thermoformed.cost"].create(
            {
                "product_id": self.material_product.id,
                "width": 500.0,
                "step": 400.0,
                "thickness": 0.8,
                "density": 1.2,
            }
        )
        self.assertAlmostEqual(cost.density, 1.2, places=4)


@tagged("post_install", "-at_install")
class TestThermoformedCostComputeWeight(ThermoformedCostCommon):
    def test_compute_weight(self):
        cost = self._create_thermoformed_cost()
        expected_plate_weight = 500.0 * 400.0 * 0.8 * 0.92 / 1000000
        self.assertAlmostEqual(
            cost.plate_weight, expected_plate_weight, places=self.dp_stock_weight
        )
        plates = 10000 / 6
        plate_per_serie = plates * (1 + 3.0 / 100)
        plate_units = plate_per_serie + 100
        expected_serie_weight = expected_plate_weight * plate_units
        self.assertAlmostEqual(
            cost.serie_weight, expected_serie_weight, places=self.dp_stock_weight
        )

    def test_compute_weight_zero_thickness(self):
        cost = self._create_thermoformed_cost(thickness=0.0)
        self.assertAlmostEqual(cost.plate_weight, 0.0, places=4)
        self.assertAlmostEqual(cost.serie_weight, 0.0, places=4)


@tagged("post_install", "-at_install")
class TestThermoformedCostComputePlateCost(ThermoformedCostCommon):
    def test_compute_plate_cost(self):
        cost = self._create_thermoformed_cost()
        expected_plate_cost = float_round(
            cost.plate_weight * cost.material_cost,
            precision_digits=self.dp_product_price,
        )
        self.assertAlmostEqual(
            cost.plate_cost, expected_plate_cost, places=self.dp_product_price
        )


@tagged("post_install", "-at_install")
class TestThermoformedCostComputeManufacturingCost(ThermoformedCostCommon):
    def test_compute_manufacturing_cost_unit(self):
        cost = self._create_thermoformed_cost()
        expected = (50.0 + 25.0 * 1.0) / (50 * 6)
        self.assertAlmostEqual(
            cost.manufacturing_cost_unit, expected, places=self.dp_product_price
        )

    def test_compute_manufacturing_cost_multiple_operators(self):
        cost = self._create_thermoformed_cost(operator=2.0)
        expected = (50.0 + 25.0 * 2.0) / (50 * 6)
        self.assertAlmostEqual(
            cost.manufacturing_cost_unit, expected, places=self.dp_product_price
        )


@tagged("post_install", "-at_install")
class TestThermoformedCostComputeAssembly(ThermoformedCostCommon):
    def test_compute_assembly_cost(self):
        cost = self._create_thermoformed_cost()
        expected_total = (50.0 + 30.0) * 2.0
        expected_unit = expected_total / 10000
        self.assertAlmostEqual(
            cost.assembly_cost, expected_total, places=self.dp_product_price
        )
        self.assertAlmostEqual(
            cost.assembly_cost_unit, expected_unit, places=self.dp_product_price
        )


@tagged("post_install", "-at_install")
class TestThermoformedCostComputePackaging(ThermoformedCostCommon):
    def test_compute_packaging_cost(self):
        cost = self._create_thermoformed_cost()
        boxes = int(10000 / 50)
        pallets = int(boxes / 16)
        expected_total = (boxes * 0.50) + (pallets * 12.0)
        expected_unit = expected_total / 10000
        self.assertAlmostEqual(
            cost.packaging_cost, expected_total, places=self.dp_product_price
        )
        self.assertAlmostEqual(
            cost.packaging_cost_unit, expected_unit, places=self.dp_product_price
        )


@tagged("post_install", "-at_install")
class TestThermoformedCostComputeTransport(ThermoformedCostCommon):
    def test_compute_transport_cost_unit(self):
        cost = self._create_thermoformed_cost()
        expected = 40.0 / (50 * 16)
        self.assertAlmostEqual(
            cost.transport_cost_unit, expected, places=self.dp_product_price
        )


@tagged("post_install", "-at_install")
class TestThermoformedCostComputeAmount(ThermoformedCostCommon):
    def test_compute_amount(self):
        cost = self._create_thermoformed_cost()
        expected = (
            (cost.plate_cost / cost.figure)
            + cost.manufacturing_cost_unit
            + cost.assembly_cost_unit
            + cost.packaging_cost_unit
            + cost.transport_cost_unit
        )
        self.assertAlmostEqual(cost.amount, expected, places=self.dp_price_unit)


@tagged("post_install", "-at_install")
class TestThermoformedCostComputeMarginCommission(ThermoformedCostCommon):
    def test_compute_margin_commission(self):
        cost = self._create_thermoformed_cost()
        expected_commission_amount = 5.0 * (1.0 / 100)
        self.assertAlmostEqual(
            cost.commission_amount,
            expected_commission_amount,
            places=self.dp_product_price,
        )
        expected_margin = (5.0 - expected_commission_amount - cost.amount) * 100 / 5.0
        self.assertAlmostEqual(cost.margin, expected_margin, places=self.dp_discount)

    def test_compute_margin_commission_zero_price(self):
        cost = self._create_thermoformed_cost(unit_retail_price=0.0)
        self.assertAlmostEqual(cost.commission_amount, 0.0, places=4)
        self.assertAlmostEqual(cost.margin, 0.0, places=4)


@tagged("post_install", "-at_install")
class TestThermoformedCostComputeMachineHour(ThermoformedCostCommon):
    def test_compute_machine_hour_serie(self):
        cost = self._create_thermoformed_cost()
        expected = 2.0 + ((10000 * (1 + 3.0 / 100)) / 6) / 50
        self.assertAlmostEqual(
            cost.machine_hour_serie, expected, places=self.dp_product_price
        )

    def test_compute_machine_hour_annual(self):
        cost = self._create_thermoformed_cost()
        expected_serie = 2.0 + ((10000 * (1 + 3.0 / 100)) / 6) / 50
        expected_annual = (expected_serie / 10000) * 10000
        self.assertAlmostEqual(
            cost.machine_hour_annual, expected_annual, places=self.dp_product_price
        )


@tagged("post_install", "-at_install")
class TestThermoformedCostComputePurchaseCost(ThermoformedCostCommon):
    def test_compute_purchase_cost(self):
        cost = self._create_thermoformed_cost()
        expected_unit_raw = (
            (cost.serie_weight * cost.material_cost / cost.serie)
            + cost.packaging_cost_unit
            + cost.transport_cost_unit
        )
        expected_unit = float_round(
            expected_unit_raw, precision_digits=self.dp_product_price
        )
        self.assertAlmostEqual(
            cost.purchase_cost_unit, expected_unit, places=self.dp_product_price
        )
        expected_serie = float_round(
            expected_unit_raw * 10000, precision_digits=self.dp_product_price
        )
        self.assertAlmostEqual(
            cost.purchase_cost_serie, expected_serie, places=self.dp_product_price
        )
        expected_annual = float_round(
            expected_unit_raw * 10000, precision_digits=self.dp_product_price
        )
        self.assertAlmostEqual(
            cost.purchase_cost_annual, expected_annual, places=self.dp_product_price
        )


@tagged("post_install", "-at_install")
class TestThermoformedCostComputeInvoicing(ThermoformedCostCommon):
    def test_compute_invoicing(self):
        cost = self._create_thermoformed_cost()
        self.assertAlmostEqual(
            cost.invoicing_serie, 5.0 * 10000, places=self.dp_product_price
        )
        self.assertAlmostEqual(
            cost.invoicing_annual, 5.0 * 10000, places=self.dp_product_price
        )


@tagged("post_install", "-at_install")
class TestThermoformedCostComputeValueAdded(ThermoformedCostCommon):
    def test_compute_value_added_unit(self):
        cost = self._create_thermoformed_cost()
        expected = cost.manufacturing_cost_unit + cost.assembly_cost_unit
        self.assertAlmostEqual(
            cost.value_added_unit, expected, places=self.dp_product_price
        )

    def test_compute_value_added_serie(self):
        cost = self._create_thermoformed_cost()
        expected = (
            cost.invoicing_serie * (1 - cost.commission / 100)
            - cost.purchase_cost_serie
        )
        self.assertAlmostEqual(
            cost.value_added_serie, expected, places=self.dp_product_price
        )

    def test_compute_value_added_hour(self):
        cost = self._create_thermoformed_cost()
        expected_serie = (
            cost.invoicing_serie * (1 - cost.commission / 100)
            - cost.purchase_cost_serie
        )
        expected_hour = expected_serie / cost.machine_hour_serie
        self.assertAlmostEqual(
            cost.value_added_hour, expected_hour, places=self.dp_product_price
        )

    def test_compute_value_added_annual(self):
        cost = self._create_thermoformed_cost()
        expected = (
            cost.invoicing_annual * (1 - cost.commission / 100)
            - cost.purchase_cost_annual
        )
        self.assertAlmostEqual(
            cost.value_added_annual, expected, places=self.dp_product_price
        )


@tagged("post_install", "-at_install")
class TestThermoformedCostComputeCostSale(ThermoformedCostCommon):
    def test_compute_cost_sale(self):
        cost = self._create_thermoformed_cost()
        expected = (cost.purchase_cost_serie / cost.invoicing_serie) * 100
        self.assertAlmostEqual(cost.cost_sales, expected, places=2)

    def test_compute_cost_sale_zero_invoicing(self):
        cost = self._create_thermoformed_cost(unit_retail_price=0.0)
        self.assertAlmostEqual(cost.cost_sales, 0.0, places=4)


@tagged("post_install", "-at_install")
class TestThermoformedCostWrite(ThermoformedCostCommon):
    def test_write_updates_density(self):
        cost = self._create_thermoformed_cost()
        new_product = self.env["product.template"].create(
            {
                "name": "New Material",
                "density": 1.5,
                "list_price": 2.0,
                "categ_id": self.product_category.id,
            }
        )
        cost.write({"product_id": new_product.id})
        self.assertAlmostEqual(cost.density, 1.5, places=4)

    def test_write_density_explicit(self):
        cost = self._create_thermoformed_cost()
        new_product = self.env["product.template"].create(
            {
                "name": "New Material",
                "density": 1.5,
                "list_price": 2.0,
                "categ_id": self.product_category.id,
            }
        )
        cost.write({"product_id": new_product.id, "density": 2.0})
        self.assertAlmostEqual(cost.density, 2.0, places=4)


@tagged("post_install", "-at_install")
class TestThermoformedCostStateTransitions(ThermoformedCostCommon):
    def test_action_block(self):
        cost = self._create_thermoformed_cost()
        self.assertEqual(cost.state, "draft")
        cost.action_block()
        self.assertEqual(cost.state, "closed")

    def test_action_draft(self):
        cost = self._create_thermoformed_cost()
        cost.action_block()
        self.assertEqual(cost.state, "closed")
        cost.action_draft()
        self.assertEqual(cost.state, "draft")


@tagged("post_install", "-at_install")
class TestThermoformedCostUnlink(ThermoformedCostCommon):
    def test_unlink_draft(self):
        cost = self._create_thermoformed_cost()
        cost.unlink()
        self.assertFalse(cost.exists())

    def test_unlink_closed_raises(self):
        cost = self._create_thermoformed_cost()
        cost.action_block()
        with self.assertRaises(ValidationError):
            cost.unlink()


@tagged("post_install", "-at_install")
class TestThermoformedCostSqlConstraints(ThermoformedCostCommon):
    def test_constraint_figure_positive(self):
        with self.assertRaises(psycopg2.errors.CheckViolation), self.cr.savepoint():
            self._create_thermoformed_cost(figure=-1)

    def test_constraint_plate_hour_positive(self):
        with self.assertRaises(psycopg2.errors.CheckViolation), self.cr.savepoint():
            self._create_thermoformed_cost(plate_hour=-1)

    def test_constraint_serie_positive(self):
        with self.assertRaises(psycopg2.errors.CheckViolation), self.cr.savepoint():
            self._create_thermoformed_cost(serie=-1)

    def test_constraint_box_quantity_positive(self):
        with self.assertRaises(psycopg2.errors.CheckViolation), self.cr.savepoint():
            self._create_thermoformed_cost(box_quantity=-1)

    def test_constraint_box_pallet_positive(self):
        with self.assertRaises(psycopg2.errors.CheckViolation), self.cr.savepoint():
            self._create_thermoformed_cost(box_pallet=-1)

    def test_constraint_adjustment_plates_positive(self):
        with self.assertRaises(psycopg2.errors.CheckViolation), self.cr.savepoint():
            self._create_thermoformed_cost(adjustment_plates=-1)

    def test_constraint_waste_percentage_positive(self):
        with self.assertRaises(psycopg2.errors.CheckViolation), self.cr.savepoint():
            self._create_thermoformed_cost(waste_percentage=-1)

    def test_constraint_name_unique(self):
        self._create_thermoformed_cost(name="DUP-001")
        with self.assertRaises(psycopg2.errors.UniqueViolation), self.cr.savepoint():
            self._create_thermoformed_cost(name="DUP-001")


@tagged("post_install", "-at_install")
class TestThermoformedCostOnchange(ThermoformedCostCommon):
    def test_onchange_product_id(self):
        cost = self.env["thermoformed.cost"].new({})
        cost.product_id = self.material_product
        cost.onchange_product_id()
        self.assertAlmostEqual(cost.density, self.material_product.density, places=4)
        self.assertAlmostEqual(
            cost.material_cost, self.material_product.list_price, places=4
        )

    def test_onchange_product_id_empty(self):
        cost = self.env["thermoformed.cost"].new({})
        cost.product_id = False
        cost.onchange_product_id()
        self.assertAlmostEqual(cost.density, 0.0, places=4)

    def test_onchange_workcenter_id(self):
        cost = self.env["thermoformed.cost"].new({})
        cost.workcenter_id = self.workcenter
        cost.onchange_workcenter_id()
        self.assertAlmostEqual(
            cost.workcenter_cost, self.workcenter.costs_hour, places=4
        )

    def test_onchange_company_id(self):
        cost = self.env["thermoformed.cost"].new({})
        cost.company_id = self.company
        cost.onchange_company_id()
        self.assertAlmostEqual(
            cost.operator_cost, self.company.costs_operator, places=4
        )
        self.assertAlmostEqual(
            cost.mechanic_cost, self.company.costs_mechanic, places=4
        )
        self.assertAlmostEqual(
            cost.margin_purchase, self.company.margin_purchase, places=4
        )
        self.assertAlmostEqual(
            cost.value_added_margin, self.company.value_added_margin, places=4
        )

    def test_onchange_box_id(self):
        cost = self.env["thermoformed.cost"].new({})
        cost.box_id = self.box_product
        cost.onchange_box_id()
        self.assertAlmostEqual(cost.box_cost, self.box_product.list_price, places=4)

    def test_onchange_pallet_id(self):
        cost = self.env["thermoformed.cost"].new({})
        cost.pallet_id = self.pallet_product
        cost.onchange_pallet_id()
        self.assertAlmostEqual(
            cost.pallet_cost, self.pallet_product.list_price, places=4
        )

    def test_onchange_frame_id(self):
        cost = self.env["thermoformed.cost"].new({})
        cost.frame_id = self.frame
        cost.onchange_frame_id()
        self.assertAlmostEqual(cost.width, self.frame.width, places=4)
        self.assertAlmostEqual(cost.step, self.frame.step, places=4)

    def test_onchange_annual_amount(self):
        cost = self.env["thermoformed.cost"].new({})
        cost.serie = 5000
        cost.onchange_annual_amount()
        self.assertEqual(cost.annual_amount, 5000)


@tagged("post_install", "-at_install")
class TestThermoformedCostFullScenario(ThermoformedCostCommon):
    def test_full_cost_calculation_consistency(self):
        cost = self._create_thermoformed_cost()
        self.assertGreater(cost.plate_weight, 0)
        self.assertGreater(cost.serie_weight, 0)
        self.assertGreater(cost.plate_cost, 0)
        self.assertGreater(cost.manufacturing_cost_unit, 0)
        self.assertGreater(cost.assembly_cost, 0)
        self.assertGreater(cost.assembly_cost_unit, 0)
        self.assertGreater(cost.packaging_cost, 0)
        self.assertGreater(cost.packaging_cost_unit, 0)
        self.assertGreater(cost.transport_cost_unit, 0)
        self.assertGreater(cost.amount, 0)
        self.assertGreater(cost.commission_amount, 0)
        self.assertGreater(cost.margin, 0)
        self.assertGreater(cost.machine_hour_serie, 0)
        self.assertGreater(cost.machine_hour_annual, 0)
        self.assertGreater(cost.purchase_cost_unit, 0)
        self.assertGreater(cost.purchase_cost_serie, 0)
        self.assertGreater(cost.invoicing_serie, 0)
        self.assertGreater(cost.value_added_unit, 0)
        self.assertGreater(cost.value_added_serie, 0)
        self.assertGreater(cost.value_added_hour, 0)
        self.assertGreater(cost.cost_sales, 0)
        self.assertLess(cost.cost_sales, 100)

    def test_amount_equals_sum_of_parts(self):
        cost = self._create_thermoformed_cost()
        total = (
            (cost.plate_cost / cost.figure)
            + cost.manufacturing_cost_unit
            + cost.assembly_cost_unit
            + cost.packaging_cost_unit
            + cost.transport_cost_unit
        )
        self.assertAlmostEqual(cost.amount, total, places=self.dp_price_unit)

    def test_invoicing_equals_price_times_quantity(self):
        cost = self._create_thermoformed_cost()
        self.assertAlmostEqual(
            cost.invoicing_serie,
            cost.unit_retail_price * cost.serie,
            places=self.dp_product_price,
        )
        self.assertAlmostEqual(
            cost.invoicing_annual,
            cost.unit_retail_price * cost.annual_amount,
            places=self.dp_product_price,
        )

    def test_cost_sales_relationship(self):
        cost = self._create_thermoformed_cost()
        self.assertAlmostEqual(
            cost.cost_sales,
            (cost.purchase_cost_serie / cost.invoicing_serie) * 100,
            places=2,
        )

    def test_value_added_hour_relationship(self):
        cost = self._create_thermoformed_cost()
        expected = cost.value_added_serie / cost.machine_hour_serie
        self.assertAlmostEqual(
            cost.value_added_hour, expected, places=self.dp_product_price
        )
