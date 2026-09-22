# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestStockMoveCost(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls.product_standard = cls.env["product.product"].create(
            {
                "name": "Test Product Standard Price",
                "type": "consu",
                "standard_price": 25.0,
            }
        )
        cls.product_no_price = cls.env["product.product"].create(
            {
                "name": "Test Product No Price",
                "type": "consu",
                "standard_price": 0.0,
            }
        )
        supplier = cls.env["res.partner"].search([("supplier_rank", ">", 0)], limit=1)
        if not supplier:
            supplier = cls.env["res.partner"].create(
                {"name": "Test Supplier", "supplier_rank": 1}
            )
        cls.purchase_product = cls.env["product.product"].create(
            {
                "name": "Test Product Purchase Price",
                "type": "consu",
                "standard_price": 10.0,
            }
        )
        po = cls.env["purchase.order"].create(
            {
                "partner_id": supplier.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": cls.purchase_product.id,
                            "name": cls.purchase_product.name,
                            "product_qty": 1.0,
                            "price_unit": 35.0,
                            "product_uom": cls.purchase_product.uom_id.id,
                        },
                    )
                ],
            }
        )
        po.button_confirm()
        for line in po.order_line:
            line.qty_received = 1.0
        cls.purchase_product.invalidate_recordset(["last_purchase_line_id"])
        picking_type = cls.env.ref("stock.picking_type_in")
        location = cls.env["stock.location"].search(
            [("usage", "=", "supplier")], limit=1
        )
        cls.location_dest = picking_type.default_location_dest_id
        cls.picking_vals = {
            "location_id": location.id,
            "location_dest_id": cls.location_dest.id,
            "picking_type_id": picking_type.id,
        }

    def _create_move_line(self, vals):
        picking = self.env["stock.picking"].create(
            {
                **self.picking_vals,
                "move_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": vals["product_id"],
                            "name": "test",
                            "product_uom_qty": vals.get("quantity", 1.0),
                            "product_uom": vals["product_uom_id"],
                        },
                    )
                ],
            }
        )
        move = picking.move_ids[0]
        move.quantity = vals.get("quantity", 1.0)
        line = move.move_line_ids[0]
        if "price_unit_cost" in vals:
            line.price_unit_cost = vals["price_unit_cost"]
        if "lot_id" in vals:
            line.lot_id = vals["lot_id"]
        return line

    def test_compute_cost_move_line(self):
        line = self._create_move_line(
            {
                "product_id": self.product_standard.id,
                "product_uom_id": self.product_standard.uom_id.id,
                "quantity": 5.0,
                "price_unit_cost": 20.0,
            }
        )
        self.assertEqual(line.cost, 100.0)
        line.quantity = 3.0
        self.assertEqual(line.cost, 60.0)
        line.price_unit_cost = 25.0
        self.assertEqual(line.cost, 75.0)

    def test_onchange_product_id_sets_cost_from_last_purchase(self):
        line = self.env["stock.move.line"].new(
            {
                "product_id": self.purchase_product.id,
                "product_uom_id": self.purchase_product.uom_id.id,
            }
        )
        line._onchange_product_id()
        self.assertEqual(line.price_unit_cost, 35.0)

    def test_onchange_product_id_fallback_standard_price(self):
        line = self.env["stock.move.line"].new(
            {
                "product_id": self.product_standard.id,
                "product_uom_id": self.product_standard.uom_id.id,
            }
        )
        line._onchange_product_id()
        self.assertEqual(line.price_unit_cost, 25.0)

    def test_create_move_line_auto_cost_from_standard_price(self):
        picking = self.env["stock.picking"].create(
            {
                **self.picking_vals,
                "move_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product_standard.id,
                            "name": "test",
                            "product_uom_qty": 2.0,
                            "product_uom": self.product_standard.uom_id.id,
                        },
                    )
                ],
            }
        )
        move = picking.move_ids[0]
        move.quantity = 2.0
        line = move.move_line_ids[0]
        self.assertEqual(line.price_unit_cost, 25.0)
        self.assertEqual(line.cost, 50.0)

    def test_create_move_line_preserves_explicit_cost(self):
        line = self._create_move_line(
            {
                "product_id": self.purchase_product.id,
                "product_uom_id": self.purchase_product.uom_id.id,
                "quantity": 2.0,
                "price_unit_cost": 10.0,
            }
        )
        self.assertEqual(line.price_unit_cost, 10.0)
        self.assertEqual(line.cost, 20.0)

    def test_write_move_line_preserves_cost(self):
        line = self._create_move_line(
            {
                "product_id": self.purchase_product.id,
                "product_uom_id": self.purchase_product.uom_id.id,
                "quantity": 2.0,
                "price_unit_cost": 10.0,
            }
        )
        self.assertEqual(line.price_unit_cost, 10.0)
        line.quantity = 5.0
        self.assertEqual(line.price_unit_cost, 10.0)
        self.assertEqual(line.cost, 50.0)

    def test_put_price_unit_cost_in_line_lot(self):
        lot = self.env["stock.lot"].create(
            {
                "product_id": self.product_standard.id,
                "name": "LOT-TEST-001",
                "purchase_price": 30.0,
            }
        )
        picking = self.env["stock.picking"].create(
            {
                **self.picking_vals,
                "move_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product_standard.id,
                            "name": "test",
                            "product_uom_qty": 1.0,
                            "product_uom": self.product_standard.uom_id.id,
                        },
                    )
                ],
            }
        )
        move = picking.move_ids[0]
        move.quantity = 1.0
        line = move.move_line_ids[0]
        line.lot_id = lot.id
        self.assertEqual(line.price_unit_cost, 30.0)

    def test_put_price_unit_cost_in_line_product(self):
        picking = self.env["stock.picking"].create(
            {
                **self.picking_vals,
                "move_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product_standard.id,
                            "name": "test",
                            "product_uom_qty": 1.0,
                            "product_uom": self.product_standard.uom_id.id,
                        },
                    )
                ],
            }
        )
        move = picking.move_ids[0]
        move.quantity = 1.0
        line = move.move_line_ids[0]
        self.assertEqual(line.price_unit_cost, 25.0)

    def test_compute_price_unit_cost_move(self):
        picking = self.env["stock.picking"].create(
            {
                **self.picking_vals,
                "move_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.purchase_product.id,
                            "name": self.purchase_product.name,
                            "product_uom_qty": 10.0,
                            "product_uom": self.purchase_product.uom_id.id,
                        },
                    )
                ],
            }
        )
        move = picking.move_ids[0]
        move.quantity = 10.0
        for line in move.move_line_ids:
            line.price_unit_cost = 5.0
        self.assertEqual(move.cost, 50.0)
        self.assertEqual(move.price_unit_cost, 5.0)

    def test_compute_price_unit_cost_move_zero_quantity(self):
        picking = self.env["stock.picking"].create(
            {
                **self.picking_vals,
                "move_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.purchase_product.id,
                            "name": self.purchase_product.name,
                            "product_uom_qty": 10.0,
                            "product_uom": self.purchase_product.uom_id.id,
                        },
                    )
                ],
            }
        )
        move = picking.move_ids[0]
        move.quantity = 0.0
        for line in move.move_line_ids:
            line.price_unit_cost = 5.0
        self.assertEqual(move.cost, 0.0)
        self.assertEqual(move.price_unit_cost, 0.0)

    def test_compute_price_unit_cost_move_multiple_lines(self):
        picking = self.env["stock.picking"].create(
            {
                **self.picking_vals,
                "move_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.purchase_product.id,
                            "name": self.purchase_product.name,
                            "product_uom_qty": 10.0,
                            "product_uom": self.purchase_product.uom_id.id,
                        },
                    )
                ],
            }
        )
        move = picking.move_ids[0]
        move.quantity = 10.0
        for line in move.move_line_ids:
            line.price_unit_cost = 0.0
        self.env["stock.move.line"].create(
            {
                "move_id": move.id,
                "product_id": self.purchase_product.id,
                "product_uom_id": self.purchase_product.uom_id.id,
                "quantity": 5.0,
                "price_unit_cost": 12.0,
                "location_id": move.location_id.id,
                "location_dest_id": move.location_dest_id.id,
            }
        )
        self.assertEqual(len(move.move_line_ids), 2)
        total_cost = sum(move.move_line_ids.mapped("cost"))
        self.assertEqual(move.cost, total_cost)
        if total_cost and move.quantity:
            self.assertEqual(move.price_unit_cost, total_cost / move.quantity)
