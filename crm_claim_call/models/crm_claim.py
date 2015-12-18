# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class CrmClaim(models.Model):
    _inherit = 'crm.claim'

    @api.multi
    def _crm_phonecall_count(self):
        for claim in self:
            claim.phonecalls_count = len(claim.phonecall_ids)

    phonecall_ids = fields.One2many(
        comodel_name='crm.phonecall', inverse_name='claim_id', string='Claim')
    phonecalls_count = fields.Integer(string='Phonecalls',
                                      compute='_crm_phonecall_count')
