# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    funding_source_count = fields.Integer(
        string='Funding Sources', compute='_compute_funding_source_count')
    funding_source_ids = fields.One2many(
        comodel_name='funding.source', string='Funding Sources',
        inverse_name='partner_id')

    @api.depends('funding_source_ids')
    def _compute_funding_source_count(self):
        for partner in self:
            partner.funding_source_count = len(partner.funding_source_ids)
