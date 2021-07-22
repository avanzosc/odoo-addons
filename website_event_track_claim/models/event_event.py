# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, _


class EventEvent(models.Model):
    _inherit = 'event.event'

    count_claims = fields.Integer(
        string='# claims', compute='_compute_count_claims')
    crm_claim_ids = fields.One2many(
        string='Claims', comodel_name='crm.claim',
        inverse_name='event_id')

    def _compute_count_claims(self):
        for event in self:
            event.count_claims = len(event.crm_claim_ids)

    def button_show_claims(self):
        if self.crm_claim_ids:
            context = self.env.context.copy()
            context.update(
                {'default_event_id': self.id})
            return {
                'name': _('Event claims'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'crm.claim',
                'context': context,
                'domain': [('id', 'in', self.crm_claim_ids.ids)]}
