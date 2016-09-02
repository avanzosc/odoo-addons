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
        dict_act_window = super(HrApplicant,
                                self).create_employee_from_applicant()
        if self.emp_id:
            self.emp_id.skill_ids = self.skill_ids
        return dict_act_window
