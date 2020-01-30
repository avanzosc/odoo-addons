# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestSaleLinePendingInfo(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestSaleLinePendingInfo, cls).setUpClass()
        cls.sale_model = cls.env['sale.order']

    def test_sale_line_pending_info(self):
        cond = [('state', 'in', ('sale', 'done'))]
        sale = self.sale_model.search(cond, limit=1)
        for line in sale.order_line:
            self.assertEquals(line.qty_pending_delivery,
                              line.product_uom_qty - line.qty_delivered)
            self.assertEquals(line.amount_pending_delivery,
                              line.qty_pending_delivery * line.price_unit)
            self.assertEquals(line.qty_pending_invoicing,
                              line.product_uom_qty - line.qty_invoiced)
            self.assertEquals(line.amount_pending_invoicing,
                              line.qty_pending_invoicing * line.price_unit)
