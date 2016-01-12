# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import api, fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    @api.multi
    def _meeting_count(self):
        for project in self:
            project.meeting_count = len(project.meeting_ids)

    meeting_count = fields.Integer(
        string='Meetings', compute='_meeting_count')
    meeting_ids = fields.One2many(
        'event.event', 'project_id', string='Meetings')


class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.multi
    def _meeting_count(self):
        for task in self:
            task.meeting_count = len(task.meeting_ids)

    @api.multi
    def _pending_meeting_count(self):
        for task in self:
            task.pending_meeting_count = len(task.meeting_ids.filtered(
                lambda x: x.state in ('draft', 'confirm')))

    meeting_count = fields.Integer(
        string='Meetings', compute='_meeting_count')
    pending_meeting_count = fields.Integer(
        string='Pending Meetings', compute='_pending_meeting_count')
    meeting_ids = fields.Many2many(
        comodel_name='event.event', relation='rel_task_event',
        column1='task_id', column2='event_id', string='Tasks')

    @api.multi
    def action_show_meetings(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'event.event',
            'view_mode': 'kanban,tree,calendar,form',
            'view_type': 'form',
            'target': 'current',
            'domain': [['id', 'in', self.meeting_ids.ids]]}
