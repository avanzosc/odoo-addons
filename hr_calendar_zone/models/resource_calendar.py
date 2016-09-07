# -*- coding: utf-8 -*-
# © 2016 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import fields, models


class ResourceCalendarAttendance(models.Model):
    _inherit = 'resource.calendar.attendance'

    zone_id = fields.Many2one(
        comodel_name='res.partner.zone', string='Zone')
    emp_id = fields.Many2one(comodel_name='hr.employee', string='Employee')
