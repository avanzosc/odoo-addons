# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestStockMovePurchaseUnitPrice(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestStockMovePurchaseUnitPrice, cls).setUpClass()
        cls.purchase_model = cls.env['purchase.order']

    def test_sale_line_pending_info(self):
        cond = [('state', '=', 'draft')]
        purchase = self.purchase_model.search(cond, limit=1)
        self.assertEqual(len(purchase.picking_ids), 0)
        purchase.button_confirm()
        self.assertEqual(len(purchase.picking_ids), 1)
        for picking in purchase.picking_ids:
            for move in picking.move_ids_without_package:
                move.quantity_done = move.product_uom_qty
                self.assertEqual(
                    move.purchase_price_unit, move.purchase_line_id.price_unit)
                self.assertEqual(
                    move.subtotal_purchase_price_unit,
                    move.purchase_line_id.price_unit * move.quantity_done)
