# -*- coding: utf-8 -*-
# © 2016 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common


class TestHrSkillsForApplicant(common.TransactionCase):

    def setUp(self):
        super(TestHrSkillsForApplicant, self).setUp()
        self.applicant = self.env.ref('hr_recruitment.hr_case_salesman0')

    def test_create_employee_with_skills(self):
        self.assertFalse(self.applicant.skill_ids)
        self.applicant.skill_ids = [(0, 0, {'name': 'Python'}),
                                    (0, 0, {'name': 'XML'})]
        self.assertEqual(len(self.applicant.skill_ids), 2)
        self.applicant.create_employee_from_applicant()
        self.assertTrue(self.applicant.emp_id)
        self.assertEqual(
            self.applicant.skill_ids, self.applicant.emp_id.skill_ids)
