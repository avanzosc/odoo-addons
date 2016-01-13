# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import api, fields, models


class EventEvent(models.Model):
    _inherit = 'event.event'

    @api.multi
    def _task_count(self):
        for event in self:
            event.task_count = len(event.task_ids)

    project_id = fields.Many2one(
        'project.project', string='Project')
    task_count = fields.Integer(
        string='Tasks', compute='_task_count')
    task_ids = fields.Many2many(
        comodel_name='project.task', relation='rel_task_event',
        column1='event_id', column2='task_id', string='Tasks')

    @api.multi
    def agenda_description(self):
        for event in self:
            if event.task_count > 0:
                agenda = "<p><strong>Agenda:</strong></p>\n<ul>\n"
                for task in event.task_ids:
                    agenda += "<li>" + task.name + "</li>\n"
                agenda += "</ul>\n"
                event.write({'description':
                             (event.description or '') + agenda})

    @api.model
    def create(self, values):
        event = super(EventEvent, self).create(values)
        if 'project_id' in values and values.get('project_id', False):
            event._add_followers_from_event_project()
        return event

    @api.multi
    def write(self, values):
        res = super(EventEvent, self).write(values)
        if 'project_id' in values and values.get('project_id', False):
            self._add_followers_from_event_project()
        return res

    def _add_followers_from_event_project(self):
        follower_obj = self.env['mail.followers']
        for event in self:
            for user in event.project_id.members:
                if (user.partner_id and user.partner_id.id not in
                        event.message_follower_ids.ids):
                    follower_obj.create({'res_model': 'event.event',
                                         'res_id': event.id,
                                         'partner_id': user.partner_id.id})
            for follower in event.project_id.message_follower_ids:
                if follower.id not in event.message_follower_ids.ids:
                    follower_obj.create({'res_model': 'event.event',
                                         'res_id': event.id,
                                         'partner_id': follower.id})
