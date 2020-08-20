# Copyright 2020 Adrian Revilla - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.addons.education.tests.common import TestEducationCommon


class TestEducationGroupReportMailListCommon(TestEducationCommon):

    @classmethod
    def setUpClass(cls):
        super(TestEducationGroupReportMailListCommon, cls).setUpClass()
        cls.partner_model = cls.env["res.partner"]
        cls.mail_mass_mailing_list_model = cls.env[
            "mail.mass_mailing.list"]
        cls.mail_mass_mailing_contact_model = cls.env[
            "mail.mass_mailing.contact"]
        cls.mail_mass_mailing_list_contact_rel_model = cls.env[
            "mail.mass_mailing.list_contact_rel"]
        cls.partner_mail_list_wizard_model = cls.env[
            "education.group.student.report.wizard"]

        cls.family = cls.partner_model.create({
            'name': 'Test Family',
            'educational_category': 'family',
            'is_company': True,
        })
        cls.student = cls.partner_model.create({
            'name': 'Test Student',
            'educational_category': 'student',
            'is_company': False,
            'parent_id': cls.family.id,
            'email': 'test@gmail.com'
        })
        cls.student_2 = cls.partner_model.create({
            'name': 'Test Student 2',
            'educational_category': 'student',
            'is_company': False,
            'parent_id': cls.family.id,
            'email': 'test2@gmail.com'
        })
        cls.progenitor = cls.partner_model.create({
            'name': 'Test Progenitor',
            'educational_category': 'progenitor',
            'is_company': False,
            'parent_id': cls.family.id,
            'email': 'test3@gmail.com'
        })
        cls.progenitor_2 = cls.partner_model.create({
            'name': 'Test Progenitor 2',
            'educational_category': 'progenitor',
            'is_company': False,
            'parent_id': cls.family.id,
            'email': 'test4@gmail.com'
        })
        cls.env["res.partner.family"].create({
            'child2_id': cls.student.id,
            'responsible_id': cls.progenitor.id,
            'family_id': cls.family.id,
            'relation': 'progenitor',
        })
        cls.group = cls.group_model.create({
            'education_code': 'TEST',
            'description': 'Test Group',
            'center_id': cls.edu_partner.id,
            'academic_year_id': cls.academic_year.id,
            'level_id': cls.edu_level.id,
            'student_ids': [(6, 0, cls.student.ids)],
        })
        cls.mailing_list_student = cls.mail_mass_mailing_list_model.create({
            "group_id": cls.group.id,
            "name": ("Test - Students"),
            "list_type": "student",
            "partner_mandatory": True,
        })
        cls.mailing_list_progenitor = cls.mail_mass_mailing_list_model.create({
            "group_id": cls.group.id,
            "name": ("Test - Progenitor"),
            "list_type": "progenitor",
            "partner_mandatory": True,
        })
        cls.mail_mass_mailing_contact_student = (
            cls.mail_mass_mailing_contact_model.create({
                "email": "student@gmail.com",
                "partner_id": cls.student.id,
                "list_ids": [(6, 0, cls.mailing_list_student.ids)]
                })
            )
        cls.mail_mass_mailing_contact_progenitor = (
            cls.mail_mass_mailing_contact_model.create({
                "email": "progenitor@gmail.com",
                "partner_id": cls.progenitor.id,
                "list_ids": [(6, 0, cls.mailing_list_progenitor.ids)]
            })
        )
        cls.mail_list_wizard_students = cls.partner_mail_list_wizard_model.create({
            "mass_mailing_list_id": cls.mailing_list_student.id
        })
