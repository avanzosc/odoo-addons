# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestAccountAnalyticLineWithProject(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestAccountAnalyticLineWithProject, cls).setUpClass()
        cls.line_model = cls.env['account.analytic.line']
        cls.project_model = cls.env['project.project']
        cond = [('analytic_account_id', '!=', False)]
        cls.project = cls.project_model.search(cond, limit=1)

    def test_account_analytic_line_with_project(self):
        vals = {
            'name': 'test_account_analytic_line_with_project',
            'account_id': self.project.analytic_account_id.id}
        line = self.line_model.create(vals)
        self.assertEqual(line.project_id, self.project)
        cond = [
            ('analytic_account_id', '!=', False),
            ('analytic_account_id', '!=', self.project.analytic_account_id.id)]
        project2 = self.project_model.search(cond, limit=1)
        line.account_id = project2.analytic_account_id.id
        self.assertEqual(line.project_id, project2)
