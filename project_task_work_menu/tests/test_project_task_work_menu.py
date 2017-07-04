# -*- coding: utf-8 -*-
# Copyright © 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestProjectTaskWorkMenu(common.TransactionCase):

    def setUp(self):
        super(TestProjectTaskWorkMenu, self).setUp()
        self.work_model = self.env['project.task.work']

    def test_project_task_work_menu(self):
        work_vals = {'project_id': self.ref('project.project_project_5'),
                     'task_id': self.ref('project.project_task_24'),
                     'user_id': self.ref('base.user_demo'),
                     'name': 'Test project_task_work menu',
                     'hours': 5}
        work = self.work_model.create(work_vals)
        self.assertEquals(work.project_manager_id, work.project_id.user_id,
                          'Bad project manager in task imputation')
        self.assertEquals(work.project_members_ids, work.project_id.members,
                          'Bad project members in task imputation')
