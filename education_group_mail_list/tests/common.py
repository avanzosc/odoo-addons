# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.addons.education.tests.common import TestEducationCommon


class TestEducationGroupMailListCommon(TestEducationCommon):

    @classmethod
    def setUpClass(cls):
        super(TestEducationGroupMailListCommon, cls).setUpClass()
        cls.partner_model = cls.env["res.partner"]
        cls.family = cls.partner_model.create({
            'name': 'Test Family',
            'educational_category': 'family',
            'is_company': True,
        })
        cls.relative = cls.partner_model.create({
            'name': 'Test Relative',
            'educational_category': 'otherrelative',
            'email': 'relative@test.com',
            'is_company': False,
            'parent_id': cls.family.id,
            'bank_ids': [
                (0, 0, {
                    'acc_number': '0123456789',
                }),
                (0, 0, {
                    'acc_number': '9876543210',
                })]
        })
        cls.student = cls.partner_model.create({
            'name': 'Test Student',
            'educational_category': 'student',
            'email': 'student@test.com',
            'is_company': False,
            'parent_id': cls.family.id,
            'child2_ids': [(0, 0, {
                'responsible_id': cls.relative.id,
                'family_id': cls.family.id,
                'relation': 'progenitor',
            })]
        })
        cls.group = cls.group_model.create({
            'education_code': 'TEST',
            'description': 'Test Group',
            'center_id': cls.edu_partner.id,
            'academic_year_id': cls.academic_year.id,
            'plan_id': cls.edu_plan.id,
            'level_id': cls.edu_level.id,
            'student_ids': [(6, 0, cls.student.ids)],
        })
