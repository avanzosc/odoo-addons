# -*- coding: utf-8 -*-
# (c) 2016 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class HrApplicant(models.Model):
    _inherit = 'hr.applicant'

    skill_ids = fields.Many2many(
        comodel_name='hr.skill', relation='skill_applicant_rel',
        column1='employee_id', column2='skill_id', string='Skills')

    @api.multi
    def create_employee_from_applicant(self):
        hr_employee_obj = self.env['hr.employee']
        vals = super(HrApplicant, self).create_employee_from_applicant()
        if vals['res_id']:
            employee = hr_employee_obj.browse(vals['res_id'])
            employee.skill_ids = self.skill_ids
        return vals
