# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestStockRunSchedulerManually(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestStockRunSchedulerManually, cls).setUpClass()
        cls.orderpoint_model = cls.env['stock.warehouse.orderpoint']
        cls.purchase_line_model = cls.env['purchase.order.line']
        cls.wiz_model = cls.env['wiz.run.stock.scheduler']

    def test_product_pricelist_item_menu1(self):
        cond = [('product_id', '!=', False)]
        group = self.orderpoint_model.search(cond, limit=1)
        cond = [('product_id', '=', group.product_id.id)]
        purchase_lines = self.purchase_line_model.search(cond)
        if purchase_lines:
            purchase_lines.unlink()
        cond = [('product_id', '=', group.product_id.id)]
        purchase_lines = self.purchase_line_model.search(cond)
        self.assertEqual(len(purchase_lines), 0)
        wiz = self.wiz_model.create({'use_new_cursor': False})
        wiz.with_context(
            active_ids=[group.id]).button_run_stock_scheduler()
        cond = [('product_id', '=', group.product_id.id)]
        purchase_lines = self.purchase_line_model.search(cond)
        self.assertNotEqual(len(purchase_lines), 0)
