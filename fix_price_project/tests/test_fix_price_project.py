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
        mark = self.mark_obj.create({
            'task_id': self.task.id,
            'product_id': self.product,
            'percent': 15,
            'amount': 1500,
        })
        self.assertTrue(mark)
        mark.create_invoice()
        self.assertEqual(mark.invoice_id, self.task.invoice_id)
        self.assertEqual(self.task.stage_id, self.end_stage)
