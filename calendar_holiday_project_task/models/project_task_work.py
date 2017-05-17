# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api, exceptions, _


class ProjectTaskWork(models.Model):
    _inherit = 'project.task.work'

    partner_calendar_day_id = fields.Many2one(
        comodel_name='res.partner.calendar.day',
        string='Employee calendar day')

    @api.model
    def create(self, values):
        user_obj = self.env['res.users']
        day_obj = self.env['res.partner.calendar.day']
        if values.get('user_id', False) and values.get('date', False):
            user = user_obj.search([('id', '=', values.get('user_id'))])
            if not user:
                raise exceptions.Warning(_("User not found"))
            cond = [('partner', '=', user.partner_id.id),
                    ('date', '=',
                     fields.Datetime.from_string(values.get('date')).date())]
            day = day_obj.search(cond, limit=1)
            if not day:
                raise exceptions.Warning(_("Calendar day not found for employe"
                                           "e '%s'.") % user.partner_id.name)
            values['partner_calendar_day_id'] = day.id
        return super(ProjectTaskWork, self).create(values)
