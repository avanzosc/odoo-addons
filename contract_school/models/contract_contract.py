# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ContractContract(models.Model):
    _inherit = 'contract.contract'

    child_id = fields.Many2one(
        comodel_name='res.partner', string='Child',
        domain=[('educational_category', '=', 'student')])
    course_id = fields.Many2one(
        comodel_name='education.course', string='Initial school course')
    school_id = fields.Many2one(
        comodel_name='res.partner', string='School',
        domain=[('educational_category', '=', 'school')])
    academic_year_id = fields.Many2one(
        comodel_name='education.academic_year', string='Academic year')
