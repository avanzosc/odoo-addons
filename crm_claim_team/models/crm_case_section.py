# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class CrmCaseSection(models.Model):
    _inherit = 'crm.case.section'

    @api.multi
    def _default_claim_stage(self):
        stages = self.env['crm.claim.stage'].search(
            [('case_default', '=', True)])
        return stages

    claim_stage_ids = fields.Many2many(
        comodel_name='crm.claim.stage', relation='section_claim_stage_rel',
        column1='section_id', column2='stage_id', string='Claim stages',
        default=_default_claim_stage)
    use_claims = fields.Boolean(string='Claims', default=True)
