# Copyright 2017 Alfredo de la fuente <alfredodelafuente@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests import common, tagged


@tagged("post_install", "-at_install")
class TestStockPickingWithAnalyticAccount(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestStockPickingWithAnalyticAccount, cls).setUpClass()
        picking_type = cls.env.ref("stock.picking_type_in")
        location = cls.env["stock.location"].search(
            [("usage", "=", "supplier")], limit=1
        )
        cls.analytic_account = cls.env["account.analytic.account"].create(
            {
                "name": "Stock picking with analytic_account",
                "partner_id": cls.env["res.partner"].search([], limit=1).id,
            }
        )
        cls.product = cls.env["product.product"].search([], limit=1)
        move_vals = {
            "product_id": cls.product.id,
            "name": cls.product.name,
            "quantity_done": 5.0,
            "product_uom": cls.product.uom_po_id.id,
        }
        picking_vals = {
            "analytic_account_id": cls.analytic_account.id,
            "location_id": location.id,
            "location_dest_id": picking_type.default_location_dest_id.id,
            "picking_type_id": picking_type.id,
            "move_lines": [(0, 0, move_vals)],
        }
        cls.picking = cls.env["stock.picking"].create(picking_vals)

    def test_stock_picking_with_analytic_account(self):
        self.picking.onchange_analytic_account_id()
        self.assertEqual(
            self.picking.partner_id.id,
            self.picking.analytic_account_id.partner_id.id,
            "BAD partner in stock picking",
        )
        self.assertEqual(
            self.analytic_account.picking_count,
            1,
            "BAD picking number for analytic account",
        )
        result = self.analytic_account.show_pickings_from_analytic_account()
        domain = "[('analytic_account_id', 'in', {})]".format(self.analytic_account.ids)
        self.assertEqual(
            str(result.get("domain")), domain, "BAD domain from analytic account"
        )
        self.picking.button_validate()
        cond = [("account_id", "=", self.analytic_account.id)]
        analytic_line = self.env["account.analytic.line"].search(cond, limit=1)
        self.assertEqual(len(analytic_line), 1, "Analytic line not generated")
