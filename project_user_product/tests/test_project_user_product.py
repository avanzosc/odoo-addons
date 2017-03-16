# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestProjectUserProduct(common.TransactionCase):

    def setUp(self):
        super(TestProjectUserProduct, self).setUp()
        self.project_model = self.env['project.project']
        self.task_model = self.env['project.task']
        self.work_model = self.env['project.task.work']
        self.line_model = self.env['account.analytic.line']
        self.product = self.browse_ref('product.product_product_5b')
        self.product.standard_price = 50.00
        self.user = self.browse_ref('base.user_demo')
        project_vals = {
            'name': 'TestProjectUserProduct',
        }
        user_product_vals = {
            'product_id': self.product.id,
            'user_id': self.user.id}
        project_vals['user_product_ids'] = [(0, 0, user_product_vals)]
        self.project = self.project_model.create(project_vals)
        task_vals = {'name': 'Task TestProjectUserProduct',
                     'project_id': self.project.id}
        work_vals = {'name': 'TestProjectUserProduct',
                     'hours': 3,
                     'user_id': self.user.id}
        task_vals['work_ids'] = [(0, 0, work_vals)]
        self.task = self.task_model.create(task_vals)

    def test_project_user_product(self):
        self.project._compute_members()
        cond = [('name', 'ilike', '%TestProjectUserProduct'),
                ('product_id', '=', self.product.id),
                ('unit_amount', '=', 3)]
        line = self.line_model.search(cond, limit=1)
        self.assertEqual(line.amount, -150.00,
                         'Bad inputation from project task work')
