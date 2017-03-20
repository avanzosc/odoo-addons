# -*- coding: utf-8 -*-
# (c) 2017 Esther Marín - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import openerp.tests.common as common
from openerp import exceptions


class TestFixPriceProject(common.TransactionCase):

    def setUp(self):
        super(TestFixPriceProject, self).setUp()
        self.end_stage = self.env.ref('project.project_tt_deployment')
        self.task = self.env.ref('project.project_task_13')
        self.mark_obj = self.env['invoice.mark']
        self.product = self.ref('product.product_product_6')
        self.partner = self.ref('base.res_partner_5')
        self.account_obj = self.env['account.invoice']
        self.end_stage.ending = True

    def test_invoice_task(self):
        self.assertNotEqual(self.task.stage_id, self.end_stage)
        # project without partner
        with self.assertRaises(exceptions.Warning):
            self.task.create_invoice()
        self.task.project_id.partner_id = self.partner
        self.assertFalse(self.task.is_mark)
        # task without marks
        with self.assertRaises(exceptions.Warning):
            self.task.create_invoice()
        mark = self.mark_obj.create({
            'task_id': self.task.id,
            'product_id': self.product,
            'percent': 15,
            'amount': 1500,
        })
        self.assertTrue(mark)
        self.assertTrue(self.task.is_mark)
        view = self.task.create_invoice()
        invoice = self.account_obj.browse(view['res_id'])
        self.assertEqual(self.task.stage_id, self.end_stage)
        self.assertTrue(invoice)
        self.assertEqual(invoice, self.task.invoice_id)

    def test_invoice_from_mark(self):
        self.task.project_id.partner_id = self.partner
        analytic_id = self.task.project_id.analytic_account_id
        analytic_id.fix_price_invoices = True
        analytic_id.amount_max = 15000
        mark = self.mark_obj.create({
            'project_id': self.task.project_id.id,
            'task_id': self.task.id,
            'product_id': self.product,
            'percent': 15,
        })
        self.assertTrue(mark)
        mark._onchange_percent()
        self.assertEqual((analytic_id.amount_max * 15)/100, mark.amount)
        mark.amount = 3000
        mark._onchange_amount()
        self.assertEqual(mark.amount*100/analytic_id.amount_max, mark.percent)
        mark1 = self.mark_obj.create({
            'project_id': self.task.project_id.id,
            'task_id': self.task.id,
            'product_id': self.product,
            'percent': 90,
        })
        with self.assertRaises(exceptions.Warning):
            self.task.project_id._check_mark_amount_and_percent()
        mark1.percent = 30
        mark1.amount = 13500
        with self.assertRaises(exceptions.Warning):
            self.task.project_id._check_mark_amount_and_percent()
        mark.create_invoice()
        self.assertEqual(mark.invoice_id, self.task.invoice_id)
        self.assertEqual(self.task.stage_id, self.end_stage)
