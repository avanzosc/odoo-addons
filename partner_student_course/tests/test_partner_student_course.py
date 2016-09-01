# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common
from openerp import fields
from dateutil.relativedelta import relativedelta


class TestPartnerStudentCourse(common.TransactionCase):

    def setUp(self):
        super(TestPartnerStudentCourse, self).setUp()
        self.course_model = self.env['partner.student.course']
        self.partner = self.env.ref('base.res_partner_1')
        today = fields.Date.from_string(fields.Date.today())
        self.partner.birthdate_date = (fields.Date.to_string(
            today + relativedelta(years=-3)))
        self.partner.student_repeated_courses = True
        count = 0
        while count <= 5:
            course_vals = {'age': count,
                           'name': str(count)}
            self.course_model.create(course_vals)
            count += 1

    def test_partner_student_course(self):
        self.partner._compute_student_course()
        self.assertNotEqual(self.partner.student_course, False,
                            'Student wihout course')
