# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp.addons.mrp_routing_cost.tests.test_mrp_routing_cost import\
    TestMrpRoutingCost


class TestMrpProductionProfit(TestMrpRoutingCost):

    def setUp(self):
        super(TestMrpProductionProfit, self).setUp()
        self.mrp_model = self.env['mrp.production']
        self.partner = self.env['res.partner'].create({
            'name': 'Test Partner',
        })
        self.production.write({
            'profit_percent': 10.0,
            'commercial_percent': 20.0,
        })
        self.sale_order = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'order_line':
            [(0, 0, {'product_id': self.production.product_id.id,
                     'product_uom': self.production.product_id.uom_id.id,
                     'product_uom_qty': 10.0})]
        })

    def test_sale_mrp_link_profit(self):
        for line in self.sale_order.order_line:
            self.assertFalse(line.mrp_production_id)
            line.action_create_mrp()
            self.assertTrue(line.mrp_production_id)
            line.mrp_production_id.action_compute()
            self.assertEquals(line.scheduled_total,
                              line.mrp_production_id.scheduled_total)
            self.assertEquals(line.scheduled_profit,
                              line.mrp_production_id.scheduled_profit)
            self.assertEquals(line.profit_percent,
                              line.mrp_production_id.profit_percent)
            self.assertEquals(line.scheduled_commercial,
                              line.mrp_production_id.scheduled_commercial)
            self.assertEquals(line.commercial_percent,
                              line.mrp_production_id.commercial_percent)
            self.assertEquals(line.scheduled_cost_total,
                              line.mrp_production_id.scheduled_cost_total)

    def test_workcenter_profit(self):
        self.production.action_compute()
        self.assertEqual(
            round(self.production.routing_total, 2),
            round(self.production.routing_hour_total +
                  self.production.routing_cycle_total +
                  self.production.routing_operator_total, 2))
        self.assertEqual(
            round(self.production.routing_cost_total, 2),
            round(self.production.routing_profit +
                  self.production.routing_total, 2))
        for workcenter in self.production.workcenter_lines:
            self.assertEqual(
                round(workcenter.profit, 2),
                round(workcenter.subtotal *
                      (self.production.profit_percent / 100), 2))
            self.assertEqual(
                round(workcenter.commercial, 2),
                round((workcenter.subtotal + workcenter.profit) *
                      (self.production.commercial_percent / 100), 2))

    def test_product_profit(self):
        self.production.action_compute()
        self.assertEqual(
            round(self.production.scheduled_cost_total, 2),
            round(self.production.scheduled_total +
                  self.production.scheduled_profit, 2))
        for line in self.production.product_lines:
            self.assertEqual(
                round(line.profit, 2),
                round(line.subtotal *
                      (self.production.profit_percent / 100), 2))
            self.assertEqual(
                round(line.commercial, 2),
                round((line.subtotal + line.profit) *
                      (self.production.commercial_percent / 100), 2))

    def test_production_commercial(self):
        self.production.action_compute()
        by_unit = self.env['mrp.config.settings']._get_parameter(
            'subtotal.by.unit')
        self.assertEqual(
            round(self.production.commercial_total, 2),
            round(self.production.production_total *
                  (self.production.commercial_percent / 100), 2))
        self.assertEqual(
            round(self.production.external_commercial_total, 2),
            round(self.production.production_total *
                  (self.production.external_commercial_percent / 100), 2))
        self.assertEqual(
            round(self.production.external_total, 2),
            round(self.production.production_total *
                  ((100 + self.production.external_commercial_percent) / 100),
                  2))
        self.assertEqual(
            round(self.production.production_total, 2),
            round((self.production.routing_cost_total +
                   self.production.scheduled_cost_total) *
                  (self.production.product_qty if by_unit else 1), 2))
        self.assertEqual(
            round(self.production.production_total_unit, 2),
            round(self.production.production_total /
                  (self.production.product_qty or 1.0), 2))
