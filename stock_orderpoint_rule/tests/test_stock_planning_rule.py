# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common
from openerp import exceptions
from openerp import fields


class TestStockPlanningRule(common.TransactionCase):

    def setUp(self):
        super(TestStockPlanningRule, self).setUp()
        self.company = self.env.ref('base.main_company')
        self.wiz_standarice_model = self.env['procurement.custom.standarice']
        self.wiz_orderpoint_model = self.env['procurement.orderpoint.compute']
        orderpoint_vals = {
            'name': 'orderpoint test',
            'warehouse_id': self.ref('stock.warehouse0'),
            'product_id': self.ref('product.product_product_28'),
            'product_min_qty': 5,
            'product_max_qty': 10,
            'qty_multiple': 1}
        self.orderpoint = self.env['stock.warehouse.orderpoint'].create(
            orderpoint_vals)
        self.today = fields.Date.from_string(fields.Date.today())

    def test_stock_planning_rule(self):
        company_vals = {'custom_stock_planning_rule': True,
                        'stock_planning_min_days': 0,
                        'stock_average_min_month': 0}
        with self.assertRaises(exceptions.ValidationError):
            self.company.write(company_vals)
        company_vals = {'custom_stock_planning_rule': True,
                        'stock_planning_min_days': 5,
                        'stock_planning_max_days': 1}
        with self.assertRaises(exceptions.ValidationError):
            self.company.write(company_vals)
        company_vals = {'custom_stock_planning_rule': True,
                        'stock_planning_min_days': 1,
                        'stock_planning_max_days': 5,
                        'stock_average_min_month': 3,
                        'stock_average_max_month': 2}
        with self.assertRaises(exceptions.ValidationError):
            self.company.write(company_vals)
        company_vals = {'custom_stock_planning_rule': True,
                        'stock_planning_min_days': 20,
                        'stock_planning_max_days': 30,
                        'stock_planning_by_date': self.today.replace(
                            year=self.today.year, month=1, day=1),
                        'stock_average_min_month': 0,
                        'stock_average_max_month': 0}
        self.company.write(company_vals)
        self.orderpoint._compute_custom_rule()
        self.assertEquals(self.orderpoint.custom_rule_min_qty, 0,
                          'Bad orderpoint custom_rule_min_qty')
        self.assertEquals(self.orderpoint.custom_rule_max_qty, 1,
                          'Bad orderpoint custom_rule_max_qty')
        self.assertEquals(self.orderpoint.average_rule_qty, 0,
                          'Bad orderpoint average_rule_qty')
        self.orderpoint.custom_qty_to_standar()
        self.assertEquals(self.orderpoint.product_min_qty,
                          self.orderpoint.custom_rule_min_qty,
                          'Bad orderpoint product_min_qty(1)')
        self.assertEquals(self.orderpoint.product_max_qty,
                          self.orderpoint.custom_rule_max_qty,
                          'Bad orderpoint product_max_qty(1)')
        wiz_orderpoint = self.wiz_orderpoint_model.create({})
        wiz_orderpoint.with_context(
            active_model='',
            active_ids=[]).procure_calculation()
        wiz_orderpoint.with_context(
            active_model='stock.warehouse.orderpoint',
            active_ids=self.orderpoint.ids).procure_calculation()
        wiz_standarice = self.wiz_standarice_model.create({})
        wiz_standarice.with_context(
            active_ids=self.orderpoint.ids).custom_qty_to_standard()
        self.assertEquals(self.orderpoint.product_min_qty,
                          self.orderpoint.custom_rule_min_qty,
                          'Bad orderpoint product_min_qty(2)')
        self.assertEquals(self.orderpoint.product_max_qty,
                          self.orderpoint.custom_rule_max_qty,
                          'Bad orderpoint product_max_qty(2)')
        wiz_standarice.with_context(
            active_ids=self.orderpoint.ids).average_qty_to_rules()
        self.assertEquals(self.orderpoint.product_min_qty, 0,
                          'Bad orderpoint product_min_qty(3)')
        self.assertEquals(self.orderpoint.product_max_qty, 0,
                          'Bad orderpoint product_max_qty(3)')
