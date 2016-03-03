# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields


class HrContract(models.Model):
    _inherit = 'hr.contract'

    holiday_calendars = fields.Many2many(
        'calendar.holiday', string='Holiday calendars')
    partner = fields.Many2one(
        comodel_name='res.partner', string='Contract employee',
        related='employee_id.address_home_id')
