# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp.tests import common
from openerp import fields
from datetime import timedelta


class TestStockValuationExtension(common.TransactionCase):

    def setUp(self):
        super(TestStockValuationExtension, self).setUp()
        self.aml_obj = self.env['account.move.line']
        self.production = self.env.ref(
            'mrp_operations_extension.mrp_production_opeext')
        val_acc = self.ref('account.stk')
        val_journal = self.ref('stock_account.stock_journal')
        self.production.product_id.cost_method = 'real'
        self.production.product_id.valuation = 'real_time'
        categ = self.production.product_id.categ_id
        categ.property_stock_account_input_categ = val_acc
        categ.property_stock_account_output_categ = val_acc
        categ.property_stock_journal = val_journal
        self.production.signal_workflow('button_confirm')
        self.production.force_production()
        self.start_date = (
            fields.Datetime.from_string(fields.Datetime.now()) -
            timedelta(hours=1))

    def test_load_real_cost_in_account_move_line(self):
        for line in self.production.workcenter_lines:
            line.signal_workflow('button_start_working')
            line.operation_time_lines[-1].start_date = self.start_date
            line.operation_time_lines[-1].end_date = (
                self.start_date + (timedelta(hours=3)))
        self.production.action_produce(
            self.production.id, self.production.product_qty, 'consume_produce')
        for move in self.production.move_created_ids2:
            aml_lines = self.aml_obj.search([('stock_move_id', '=', move.id)])
            self.assertTrue(aml_lines)
            amount = sum(move.mapped('quant_ids.inventory_value'))
            self.assertEqual(sum(aml_lines.mapped('credit')), amount)
            self.assertEqual(sum(aml_lines.mapped('debit')), amount)
