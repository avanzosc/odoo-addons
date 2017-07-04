# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api


class ProjectTaskWork(models.Model):
    _inherit = 'project.task.work'

    @api.multi
    @api.depends('project_id', 'project_id.user_id', 'project_id.members')
    def _compute_project_info(self):
        for i in self.filtered(lambda x: x.project_id):
            i.project_manager_id = i.project_id.user_id
            i.project_members_ids = [(6, 0, i.project_id.members.ids)]

    project_id = fields.Many2one(
        comodel_name='project.project', string='Project')
    project_manager_id = fields.Many2one(
        comodel_name='res.users', string='Project manager',
        compute='_compute_project_info', store=True)
    project_members_ids = fields.Many2many(
        comodel_name='res.users', string='Project members',
        compute='_compute_project_info', store=True)
    user_id = fields.Many2one(
        comodel_name='res.users', default=False)
