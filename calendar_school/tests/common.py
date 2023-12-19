# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.addons.contacts_school_education.tests.common import\
    TestContactsSchoolEducationCommon


class TestCalendarSchoolCommon(TestContactsSchoolEducationCommon):

    @classmethod
    def setUpClass(cls):
        super(TestCalendarSchoolCommon, cls).setUpClass()
        cls.employee_model = cls.env['hr.employee']
        cls.tutor_model = cls.env['hr.employee.supervised.year']
        cls.agenda_model = cls.env['education.order.day']
        cls.calendar_model = cls.env['calendar.event']
        cls.wizard_model = cls.env['wiz.generate.meeting.from.tutoring']
        cls.wizard2_model = cls.env['wiz.change.teacher.calendar.event']
        cls.group.write({
            "student_ids": [(6, 0, cls.student.ids)],
        })
        cls.progenitor = cls.partner_model.create({
            "name": "Test Progenitor",
            "educational_category": "progenitor",
            "is_company": True,
            "responsible_ids": [(0, 0, {
                "family_id": cls.family.id,
                "child2_id": cls.student.id,
            })]
        })
        cls.teacher2 = cls.employee_model.create({
            'name': 'Teacher 2',
            'user_id': cls.env.ref('base.user_admin').id,
        })
        cls.tutor = cls.tutor_model.create({
            'student_id': cls.student.id,
            'teacher_id': cls.teacher.id,
            'school_year_id': cls.academic_year.id,
        })
        months = cls.env['base.month'].search([
            '|', ('number', '=', cls.academic_year.date_start.month),
            ('number', '=', cls.academic_year.date_end.month)])
        cls.agendas = cls.agenda_model
        types = cls.agenda_model.fields_get(
            allfields=['type'])['type']['selection']
        for month in months:
            for agenda_type in types:
                cls.agendas |= cls.agenda_model.create({
                    'month_id': month.id,
                    'school_id': cls.edu_partner.id,
                    'course_id': cls.edu_course.id,
                    'type': agenda_type[0],
                    'order_day': '{} {}'.format(agenda_type[1], month.name)
                })
