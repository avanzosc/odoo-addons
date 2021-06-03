# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, _


class CrmClaim(models.Model):
    _inherit = 'crm.claim'

    def _compute_count_phonecall_inbound(self):
        for call in self:
            call.count_phonecall_inbound = len(
                call.phonecall_inbound_ids)

    def _compute_phonecall_inbound_ids(self):
        for claim in self.filtered(lambda x: x.phonecall_inbound_id):
            cond = ['|', ('id', '=', claim.phonecall_inbound_id.id),
                    ('claim_id', '=', claim.id)]
            inbounds = self.env['crm.phonecall.inbound'].search(cond)
            claim.phonecall_inbound_ids = [(6, 0, inbounds.ids)]

    phonecall_inbound_ids = fields.Many2many(
        string="Phone call inbound",
        comodel_name="crm.phonecall.inbound",
        compute="_compute_phonecall_inbound_ids")
    count_phonecall_inbound = fields.Integer(
        '# Phone call inbound', compute='_compute_count_phonecall_inbound')
    phonecall_inbound_id = fields.Many2one(
        string='Phone call inbound', comodel_name='crm.phonecall.inbound')

    def action_view_phonecall_inbound(self):
        context = self.env.context.copy()
        context.update({'default_claim_id': self.id})
        if self.partner_id:
            context.update({'default_partner_id': self.partner_id.id})
        return {
            'name': _("Inbound phone calls"),
            'view_mode': 'tree,form',
            'res_model': 'crm.phonecall.inbound',
            'domain': [('id', 'in', self.phonecall_inbound_ids.ids)],
            'type': 'ir.actions.act_window',
            'context': context,
        }
