# -*- coding: utf-8 -*-
# © 2014-2016 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    claim_count = fields.Integer(
        string='Claims', compute='_compute_claim_count')
    claim_ids = fields.One2many(
        comodel_name='crm.claim', inverse_name='project_id', string='Claims')

    @api.depends('claim_ids')
    def _compute_claim_count(self):
        for record in self:
            record.claim_count = len(record.claim_ids)


class ProjectTask(models.Model):
    _inherit = 'project.task'

    claim_count = fields.Integer(
        string='Claims', compute='_compute_claim_count')
    claim_ids = fields.One2many(
        comodel_name='crm.claim', inverse_name='task_id', string='Claims')

    @api.depends('claim_ids')
    def _compute_claim_count(self):
        for record in self:
            record.claim_count = len(record.claim_ids)
