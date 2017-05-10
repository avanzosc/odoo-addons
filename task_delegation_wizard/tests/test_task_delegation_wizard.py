# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestTaskDelegationWizard(common.TransactionCase):

    def setUp(self):
        super(TestTaskDelegationWizard, self).setUp()
        self.wiz_delegate_model = self.env['project.task.delegate']
        self.task = self.browse_ref('project.project_task_15')

    def test_task_delegation_wizard(self):
        delegate_vals = {
            'name': 'User Interface design',
            'project_id': self.ref('project.project_project_3'),
            'user_id': self.ref('base.user_demo'),
            'split_in': 1,
            'planned_hours': 54,
            'prefix': 'CONSULTAR: User Interface design',
            'planned_hours_me': 1}
        wiz_delegate = self.wiz_delegate_model.create(delegate_vals)
        res = wiz_delegate.with_context(active_id=self.task.id).default_get(
            ['new_task_description', 'planned_hours_me', 'user_id', 'name',
             'split_in', 'prefix', 'task_planned_hours', 'state',
             'task_planned_hours_me', 'project_id', 'planned_hours'])
        self.assertEquals(res.get('planned_hours_me'), 1.0,
                          'Bad planned_hours_me')
        self.assertEquals(res.get('split_in'), 1,
                          'Bad split_in')
        self.assertEquals(res.get('state'), 'pending',
                          'Bad state')
        res = wiz_delegate.onchange_split_in(1, 55.0, 1.0)
        value = res.get('value')
        self.assertEquals(value.get('planned_hours'), 54.0,
                          'Bad planned_hours')
        self.assertEquals(value.get('task_planned_hours_me'), 1.0,
                          'Bad task_planned_hours_me')
        wiz_delegate.with_context(active_id=self.task.id).delegate()
        self.assertEquals(len(self.task.child_ids), 1,
                          'Bad delegation')
