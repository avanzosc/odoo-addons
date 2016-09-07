# -*- coding: utf-8 -*-
# © 2016 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common


class TestHrRecruitmentZone(common.TransactionCase):

    def setUp(self):
        super(TestHrRecruitmentZone, self).setUp()
        self.applicant = self.env.ref('hr_recruitment.hr_case_salesman0')
        self.applicant.zone_ids = [(6, 0, [
            self.ref('partner_zone.zone1'),
            self.ref('partner_zone.zone2'),
            self.ref('partner_zone.zone3'),
        ])]
        self.partner_id = self.env['res.partner'].create({
            'name': 'Enrique Jones',
        })
        self.applicant.partner_id = self.partner_id.id

    def test_applicant_to_employee_to_contract_zone(self):
        self.assertEqual(len(self.applicant.zone_ids), 3)
        self.applicant.create_employee_from_applicant()
        self.assertTrue(self.applicant.emp_id)
        self.assertEqual(
            self.applicant.emp_id.zone_ids, self.applicant.zone_ids)
        self.assertEqual(
            self.applicant.partner_id.zone_ids, self.applicant.zone_ids)
