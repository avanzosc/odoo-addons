# -*- coding: utf-8 -*-
# © 2016 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    zone_ids = fields.Many2many(
        comodel_name='res.partner.zone', relation='rel_zone_employee',
        column1='zone_id', column2='employee_id', string='Zones')


class HrApplicant(models.Model):
    _inherit = 'hr.applicant'

    zone_ids = fields.Many2many(
        comodel_name='res.partner.zone', relation='rel_zone_applicant',
        column1='zone_id', column2='applicant_id', string='Zones')

    @api.multi
    def create_employee_from_applicant(self):
        dict_act_window = super(HrApplicant,
                                self).create_employee_from_applicant()
        if self.emp_id:
            self.emp_id.zone_ids = self.zone_ids
            self.partner_id.zone_ids = self.zone_ids
        return dict_act_window
