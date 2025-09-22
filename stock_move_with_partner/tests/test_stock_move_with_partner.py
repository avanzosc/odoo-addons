# Copyright (c) 2020 Alfredo de la Fuente - Avanzosc S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import TransactionCase, tagged  


@tagged('post_install', '-at_install')
class TestStockMoveWithPartner(TransactionCase):  
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        picking_type = cls.env.ref("stock.picking_type_in")
        location = cls.env["stock.location"].search(
            [("usage", "=", "supplier")], limit=1
        )
        cls.product = cls.env["product.product"].search([], limit=1)
        move_vals = {
            "product_id": cls.product.id,
            "name": cls.product.name,
            "product_uom_qty": 5.0,  
            "product_uom": cls.product.uom_po_id.id,
        }
        picking_vals = {
            "location_id": location.id,
            "location_dest_id": picking_type.default_location_dest_id.id,
            "picking_type_id": picking_type.id,
            "move_ids": [(0, 0, move_vals)], 
        }
        cls.picking = cls.env["stock.picking"].create(picking_vals)

    def test_stock_move_with_partner(self):
        self.assertEqual(
            self.picking.partner_id, 
            self.picking.move_ids[0].partner_id  
        )