# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestStockPlanningRule(common.TransactionCase):

    def setUp(self):
        super(TestStockPlanningRule, self).setUp()
        self.company = self.env.ref('base.main_company')
        self.company.write({'custom_stock_planning_rule': True,
                            'stock_planning_min_days': 20,
                            'stock_planning_max_days': 60})
        self.procurement = self.env.ref(
            'stock.stock_warehouse_orderpoint_shop1_cpu1')
        self.wiz_orderpoint = self.env[
            'procurement.orderpoint.compute'].create({})
        self.wiz_orderpoint.selected_procure_calculation()

    def test_stock_planning_rule(self):
        orderpoint = self.env['stock.warehouse.orderpoint'].search([])
        orderpoint = orderpoint.filtered(
            lambda r: r.custom_rule_min_qty > 0 or r.custom_rule_max_qty > 0)
        self.assertNotEqual(
            len(orderpoint), 0, 'Not generated custom rules for planning')
