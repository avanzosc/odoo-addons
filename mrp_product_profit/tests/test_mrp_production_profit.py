# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp.addons.mrp_routing_cost.tests.test_mrp_routing_cost import\
    TestMrpRoutingCost


class TestMrpProductionProfit(TestMrpRoutingCost):

    def setUp(self):
        super(TestMrpProductionProfit, self).setUp()
        self.mrp_model = self.env['mrp.production']
        self.sale = self.env.ref('sale.sale_order_6')
        self.mrp_production.write({
            'profit_percent': 10.0,
            'commercial_percent': 20.0,
        })

    def test_product_lines_profit_commercial(self):
        self.mrp_production.action_compute()
        for line in self.mrp_production.product_lines:
            self.assertEqual(
                round(line.subtotal *
                      (self.mrp_production.profit_percent / 100), 2),
                round(line.profit, 2))
            self.assertEqual(
                round((line.subtotal + line.profit) *
                      (self.mrp_production.commercial_percent / 100), 2),
                round(line.commercial, 2))

    def test_workorder_lines_profit_commercial(self):
        self.mrp_production.action_compute()
        for line in self.mrp_production.workcenter_lines:
            self.assertEqual(
                round(line.subtotal *
                      (self.mrp_production.profit_percent / 100), 2),
                round(line.profit, 2))
            self.assertEqual(
                round((line.subtotal + line.profit) *
                      (self.mrp_production.commercial_percent / 100), 2),
                round(line.commercial, 2))
