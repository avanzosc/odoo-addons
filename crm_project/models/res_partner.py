# -*- coding: utf-8 -*-
# © 2016 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    project_ids = fields.One2many(
        comodel_name='project.project', inverse_name='partner_id',
        string='Projects')
    project_count = fields.Integer(
        compute='_compute_project_count', string='# Projects')

    @api.depends('project_ids')
    def _compute_project_count(self):
        for partner in self:
            partner.project_count = len(partner.project_ids)
