# -*- coding: utf-8 -*-
# © 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models, api, _


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    @api.multi
    def _employee_pickings_count(self):
        picking_obj = self.env['stock.picking']
        for employee in self:
            employee.picking_count = 0
            if employee.address_home_id:
                cond = [('partner_id', '=', employee.address_home_id.id)]
                pickings = picking_obj.search(cond)
                employee.picking_count = len(pickings)

    picking_count = fields.Integer(
        string='# Pickings', compute='_employee_pickings_count')

    @api.multi
    def pickings_from_employee(self):
        self.ensure_one()
        return {'name': _('Pickings'),
                'view_type': 'form',
                "view_mode": 'tree,form,calendar',
                'res_model': 'stock.picking',
                'type': 'ir.actions.act_window',
                'domain': [('partner_id', '=', self.address_home_id.id)]}
