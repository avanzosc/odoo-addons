# -*- coding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

from openerp import api, fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    @api.depends('meeting_ids')
    def _compute_meeting_count(self):
        for project in self:
            project.meeting_count = len(project.meeting_ids)

    meeting_count = fields.Integer(
        compute='_compute_meeting_count', string='Meetings')
    meeting_ids = fields.One2many(
        comodel_name='event.event', inverse_name='project_id',
        string='Meetings')


class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.depends('meeting_ids', 'meeting_ids.state')
    def _compute_meeting_count(self):
        for task in self:
            task.meeting_count = len(task.meeting_ids)
            task.pending_meeting_count = len(
                task.meeting_ids.filtered(lambda x:
                                          x.state in ('draft', 'confirm')))

    meeting_count = fields.Integer(
        compute='_compute_meeting_count', string='Meetings')
    pending_meeting_count = fields.Integer(
        compute='_compute_meeting_count', string='Pending Meetings')
    meeting_ids = fields.Many2many(
        comodel_name='event.event', relation='rel_task_event',
        column1='task_id', column2='event_id', string='Tasks')

#    _order = "priority desc, sequence, date_start, name, id"

    @api.multi
    def action_show_meetings(self):
        meetings = self.env['event.event'].search(
            [('task_ids', 'in', self.ids)])
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'event.event',
            'view_mode': 'kanban,tree,calendar,form',
            'view_type': 'form',
            'target': 'current',
            'domain': [['id', 'in', meetings.ids]],
            'res_id': meetings.ids,
        }
