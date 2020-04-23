# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields
from odoo.tests import common


class TestCalendarSchoolCommon(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestCalendarSchoolCommon, cls).setUpClass()
        cls.today = fields.Date.today()
        cls.partner_model = cls.env['res.partner']
        cls.employee_model = cls.env['hr.employee']
        cls.tutor_model = cls.env['hr.employee.supervised.year']
        cls.agenda_model = cls.env['education.order.day']
        cls.wizard_model = cls.env['wiz.generate.meeting.from.tutoring']
        cls.calendar_model = cls.env['calendar.event']
        cls.wizard2_model = cls.env['wiz.change.teacher.calendar.event']
        today_year = cls.today.year
        start = cls.today.replace(year=today_year + 10, month=9, day=1)
        end = cls.today.replace(year=today_year + 11, month=7, day=31)
        cls.academic_year = cls.env['education.academic_year'].create({
            'name': '{}+{}'.format(start.year, end.year),
            'date_start': start,
            'date_end': end,
        })
        cls.family = cls.partner_model.create({
            'name': 'Family',
            'educational_category': 'family',
        })
        cls.progenitor = cls.partner_model.create({
            'name': 'Parent',
            'educational_category': 'progenitor',
        })
        cls.student = cls.partner_model.create({
            'name': 'Student',
            'educational_category': 'student',
            'child2_ids': [(0, 0, {
                'responsible_id': cls.progenitor.id,
                'family_id': cls.family.id,
            })],
        })
        cls.center = cls.partner_model.create({
            'name': 'Center',
            'educational_category': 'school',
        })
        cls.teacher = cls.employee_model.create({
            'name': 'Teacher',
            'user_id': cls.env.ref('base.user_admin').id,
        })
        cls.tutor = cls.tutor_model.create({
            'student_id': cls.student.id,
            'teacher_id': cls.teacher.id,
            'school_year_id': cls.academic_year.id,
        })
        cls.edu_plan = cls.env['education.plan'].create({
            'education_code': 'TEST',
            'description': 'Test Plan',
        })
        cls.edu_level = cls.env['education.level'].create({
            'education_code': 'TEST',
            'description': 'Test Level',
            'plan_id': cls.edu_plan.id,
        })
        cls.edu_course = cls.env['education.course'].create({
            'education_code': 'TEST',
            'description': 'Test Course',
            'plan_id': cls.edu_plan.id,
            'level_id': cls.edu_level.id,
        })
        cls.group_type = cls.env['education.group_type'].create({
            'education_code': 'TEST',
            'description': 'TEST',
            'type': 'official',
        })
        cls.group = cls.env['education.group'].create({
            'education_code': 'TEST',
            'description': 'Test Group',
            'center_id': cls.center.id,
            'academic_year_id': cls.academic_year.id,
            'level_id': cls.edu_level.id,
            'course_id': cls.edu_course.id,
            'student_ids': [(6, 0, cls.student.ids)],
            'group_type_id': cls.group_type.id,
        })
        months = cls.env['base.month'].search([
            '|', ('number', '=', start.month), ('number', '=', end.month)])
        cls.agendas = cls.agenda_model
        types = cls.agenda_model.fields_get(
            allfields=['type'])['type']['selection']
        for month in months:
            for agenda_type in types:
                cls.agendas |= cls.agenda_model.create({
                    'month_id': month.id,
                    'school_id': cls.center.id,
                    'course_id': cls.edu_course.id,
                    'type': agenda_type[0],
                    'order_day': '{} {}'.format(agenda_type[1], month.name)
                })
        cls.teacher2 = cls.employee_model.create({
            'name': 'Teacher 2',
            'user_id': cls.env.ref('base.user_admin').id,
        })
        cls.tutor2 = cls.tutor_model.create({
            'student_id': cls.student.id,
            'teacher_id': cls.teacher2.id,
            'school_year_id': cls.academic_year.id,
        })
