# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class EducationGroupStudentProgenitorReport(models.Model):
    _name = 'education.group.student.progenitor.report'
    _inherit = 'education.group.student.report'

    progenitor_ids = fields.Many2many(
        comodel_name='res.partner',string='Progenitors',
        relation='rel_student_progenitor', column1='progenitor_id', column2='student_id')
    
