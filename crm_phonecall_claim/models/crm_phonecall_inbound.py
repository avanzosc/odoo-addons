# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, _


class CrmPhonecallInbound(models.Model):
    _inherit = 'crm.phonecall.inbound'

    def _compute_count_claim(self):
        for claim in self:
            claim.count_claim = len(
                claim.claim_ids)

    def _compute_claim_ids(self):
        for inbound in self:
            cond = ['|', ('id', '=', inbound.claim_id.id), (
                'phonecall_inbound_id', '=', inbound.id)]
            claims = self.env['crm.claim'].search(cond)
            inbound.claim_ids = [(6, 0, claims.ids)]

    claim_ids = fields.Many2many(
        string="Claims",
        comodel_name="crm.claim",
        compute='_compute_claim_ids')
    count_claim = fields.Integer('# Claim', compute='_compute_count_claim')
    claim_id = fields.Many2one(
        string='Claim', comodel_name='crm.claim')

    def action_view_claim(self):
        context = self.env.context.copy()
        context.update({'default_phonecall_inbound_id': self.id})
        if self.partner_id:
            context.update({'default_partner_id': self.partner_id.id})
        return {
            'name': _("Claims"),
            'view_mode': 'tree,calendar,form',
            'res_model': 'crm.claim',
            'domain': [('id', 'in', self.claim_ids.ids)],
            'type': 'ir.actions.act_window',
            'context': context,
        }
