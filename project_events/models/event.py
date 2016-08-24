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


class EventEvent(models.Model):
    _inherit = 'event.event'

    @api.depends('task_ids')
    def _compute_task_count(self):
        for event in self:
            event.task_count = len(event.task_ids)

    project_id = fields.Many2one(
        comodel_name='project.project', string='Project')
    task_count = fields.Integer(compute='_compute_task_count', string='Tasks')
    task_ids = fields.Many2many(
        comodel_name='project.task', relation='rel_task_event',
        column1='event_id', column2='task_id', string='Tasks')

    @api.multi
    def agenda_description(self):
        for event in self.filtered(lambda e: e.task_count > 0):
            agenda = "<p><strong>Agenda:</strong></p>\n<ul>\n"
            for task in event.task_ids:
                agenda += "<li>" + task.name + "</li>\n"
            agenda += "</ul>\n"
            event.write({'description': (event.description or '') + agenda})
        return True
