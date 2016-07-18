# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields


class PartnerStudentCourse(models.Model):
    _name = 'partner.student.course'
    _description = 'Students courses'
    _order = 'age asc'

    name = fields.Char(string='Description', requited=True)
    age = fields.Integer(
        string='age', required=True, help="Student's age to be in the course")
