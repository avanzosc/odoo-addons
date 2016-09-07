# -*- coding: utf-8 -*-
# © 2016 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class ResourceCalendarAttendance(models.Model):
    _inherit = 'resource.calendar.attendance'

    zone_id = fields.Many2one(
        comodel_name='res.partner.zone', string='Zone')
    emp_id = fields.Many2one(comodel_name='hr.employee', string='Employee')

    @api.onchange('emp_id')
    def onchange_emp_id(self):
        if self.emp_id:
            return {'domain': {'zone_id': [
                    ('id', 'in', self.emp_id.address_home_id.zone_ids.ids)]}}
