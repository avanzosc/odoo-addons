# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestQcInspectionFromEmployee(common.TransactionCase):

    def setUp(self):
        super(TestQcInspectionFromEmployee, self).setUp()
        self.inspection_model = self.env['qc.inspection']
        self.employee = self.env.ref('hr.employee_al')
        inspection_vals = {'object_id': ('hr.employee,' +
                                         str(self.employee.id))}
        self.inspection = self.inspection_model.create(inspection_vals)

    def test_qc_inspection_from_employe(self):
        self.employee.inspections_from_employee()
        self.assertNotEqual(
            self.employee.inspections_count, 0,
            'Employee without inspections')
