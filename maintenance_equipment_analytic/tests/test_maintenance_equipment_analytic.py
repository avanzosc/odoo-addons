# Copyright (c) 2018 Alfredo de la fuente <alfredodelafuente@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests import common


class TestMaintenanceEquipmentAnalytic(common.TransactionCase):

    def setUp(self):
        super(TestMaintenanceEquipmentAnalytic, self).setUp()
        self.account = self.env['account.analytic.account'].create({
            'name': 'Analytic account for equipment'})
        self.equipment = self.env['maintenance.equipment'].create({
            'name': 'Equipment test',
            'account_analytic_id': self.account.id})
        self.line = self.env['account.analytic.line'].create({
            'name': 'Analytic entries for employee',
            'account_id': self.account.id})

    def test_hr_employee_analytic_entries(self):
        self.assertEqual(
            self.equipment.analytic_entries_count, 1,
            'BAD entries number for equipment')
        result = self.equipment.show_analytic_entries_from_equipment()
        domain = "[('id', 'in', [{}])]".format(self.line.id)
        self.assertEqual(
            str(result.get('domain')), domain, 'BAD domain from equipment')
