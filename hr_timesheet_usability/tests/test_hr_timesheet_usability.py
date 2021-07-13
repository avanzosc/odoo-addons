# Copyright 2021 Afredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests import common
from odoo import fields


@common.at_install(False)
@common.post_install(True)
class TestHrTimesheetUsability(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestHrTimesheetUsability, cls).setUpClass()
        analytic_vals1 = {
            'date': '2021-07-12 14:00:00',
            'date_end': '2021-07-13 14:00:00',
            'name': 'aaaa',
            'project_id': cls.env['project.project'].search(
                [], limit=1).id}
        analytic_vals2 = {
            'date': '2021-07-12 14:00:00',
            'name': 'bbbb',
            'project_id': cls.env['project.project'].search([], limit=1).id}
        task_vals = {
            'name': 'abcd',
            'user_id': cls.env['hr.employee'].search([], limit=1).user_id.id,
            'project_id': cls.env['project.project'].search([], limit=1).id}
        cls.analytic1 = cls.env['account.analytic.line'].create(analytic_vals1)
        cls.analytic2 = cls.env['account.analytic.line'].create(analytic_vals2)
        cls.task = cls.env['project.task'].create(task_vals)

    def test_project_task_event(self):
        self.analytic1.onchange_dates()
        self.date = fields.Datetime.now()
        self.assertEqual(self.analytic1.unit_amount, 24.0)
        self.analytic2.action_button_end()
        self.assertEqual(self.analytic2.date_end, self.date)
        self.task.action_button_initiate_task()
        self.task.action_button_end_task()
        self.assertEqual(len(self.task.timesheet_ids), 1)
        self.assertEqual(self.task.timesheet_ids.date_end, self.date)
