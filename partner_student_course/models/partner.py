# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def _compute_student_course(self):
        course_obj = self.env['partner.student.course']
        for partner in self.filtered(lambda x: x.birthdate_date):
            partner.student_age = 0
            partner.student_course = False
            today = fields.Date.context_today(self)
            today_month = fields.Date.from_string(today).month
            partner.student_age = (
                fields.Date.from_string(today).year -
                fields.Date.from_string(partner.birthdate_date).year)
            if today_month < 9:
                partner.student_age -= 1
            if partner.student_repeated_courses:
                partner.student_age -= partner.student_repeated_courses
            cond = [('age', '=', partner.student_age)]
            course = course_obj.search(cond, limit=1)
            if course:
                partner.student_course = course

    student_age = fields.Integer(
        string='Student age', compute='_compute_student_course')
    student_repeated_courses = fields.Integer(
        string='Repeated courses')
    student_course = fields.Many2one(
        comodel_name='partner.student.course', string='Student course',
        compute='_compute_student_course')
    student_class = fields.Char(string='Class')
    student_rockbotic_level = fields.Char(string='Rockbotic level')
