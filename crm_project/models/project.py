# -*- coding: utf-8 -*-
# © 2016 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    meeting_ids = fields.One2many(
        comodel_name='calendar.event', inverse_name='project_id',
        string='Meetings')
    meeting_count = fields.Integer(
        compute='_compute_meeting_count', string='# Meetings')
    phonecall_ids = fields.One2many(
        comodel_name='crm.phonecall', inverse_name='project_id',
        string='Calls')
    phonecall_count = fields.Integer(
        compute='_compute_phonecall_count', string='# Calls')

    @api.depends('meeting_ids')
    def _compute_meeting_count(self):
        for project in self:
            project.meeting_count = len(project.meeting_ids)

    @api.depends('phonecall_ids')
    def _compute_phonecall_count(self):
        for project in self:
            project.phonecall_count = len(project.phonecall_ids)
