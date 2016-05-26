# -*- coding: utf-8 -*-
# © 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models, api, _


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    @api.multi
    def _employee_inspections_count(self):
        inspection_obj = self.env['qc.inspection']
        for employee in self:
            employee.inspections_count = 0
            cond = [('object_id', '=', 'hr.employee,' + str(employee.id))]
            inspections = inspection_obj.search(cond)
            employee.inspections_count = len(inspections)

    inspections_count = fields.Integer(
        string='# Inspection', compute='_employee_inspections_count')

    @api.multi
    def inspections_from_employee(self):
        inspection_obj = self.env['qc.inspection']
        self.ensure_one()
        cond = [('object_id', '=', 'hr.employee,' + str(self.id))]
        inspections = inspection_obj.search(cond)
        return {'name': _('Inspections'),
                'view_type': 'form',
                "view_mode": 'tree,form',
                'res_model': 'qc.inspection',
                'type': 'ir.actions.act_window',
                'domain': [('id', 'in', inspections.ids)]}
