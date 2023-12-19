# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestStockMoveSaleUnitPrice(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestStockMoveSaleUnitPrice, cls).setUpClass()
        cls.sale_model = cls.env['sale.order']

    def test_sale_line_pending_info(self):
        cond = [('state', '=', 'draft')]
        sale = self.sale_model.search(cond, limit=1)
        sale.order_line.write({'discount': 10})
        self.assertEqual(len(sale.picking_ids), 0)
        sale.action_confirm()
        self.assertEqual(len(sale.picking_ids), 1)
        for picking in sale.picking_ids:
            for move in picking.move_ids_without_package:
                move.quantity_done = move.product_uom_qty
                self.assertEqual(
                    move.pvp_price_unit, move.sale_line_id.price_reduce)
                self.assertEqual(
                    move.subtotal_pvp_price_unit,
                    move.sale_line_id.price_reduce * move.quantity_done)
