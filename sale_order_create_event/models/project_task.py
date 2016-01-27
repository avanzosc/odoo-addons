# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api, _


class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.multi
    def _calc_num_sessions(self):
        for task in self:
            task.num_sessions = len(task.sessions)

    sessions = fields.Many2many(
        comodel_name="event.track", relation="task_session_project_relation",
        column1="task_id", column2="track_id", copy=False, string="Sessions")
    num_sessions = fields.Integer(
        string='# Session', compute='_calc_num_sessions')

    @api.multi
    def show_sessions_from_task(self):
        self.ensure_one()
        return {'name': _('Sessions'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree, form',
                'res_model': 'event.track',
                'domain': [('id', 'in', self.sessions.ids)]}
