# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class WizEventRegistrationCancelParticipant(models.TransientModel):
    _name = 'wiz.event.participant.create.claim'
    _description = 'Wizard for create event participant claim'

    name = fields.Text(string='Claim description')
    categ_id = fields.Many2one(
        string='Claim type', comodel_name='crm.claim.category')
    event_track_id = fields.Many2one(
        string='Event track', comodel_name='event.track')
    from_session = fields.Boolean(
        string='From session')

    @api.onchange("categ_id")
    def onchange_categ_id(self):
        if self.categ_id:
            self.name = self.categ_id.name

    def action_create_claim(self):
        self.ensure_one()
        partners = self.env['res.partner'].browse(
            self.env.context.get('active_ids'))
        for partner in partners:
            vals = {'name': self.categ_id.name,
                    'description': self.name,
                    'categ_id': self.categ_id.id,
                    'partner_id': partner.id,
                    'event_id': self.event_track_id.event_id.id,
                    'event_track_id': self.event_track_id.id}
            if (partner.phone or
               (partner.parent_id and partner.parent_id.phone)):
                vals['partner_phone'] = (
                    partner.parent_id.phone if partner.parent_id and
                    partner.parent_id.phone else partner.phone)
            if (partner.email or
               (partner.parent_id and partner.parent_id.email)):
                vals['email_from'] = (
                    partner.parent_id.email if partner.parent_id and
                    partner.parent_id.email else partner.email)
            if self.categ_id.team_id:
                vals['team_id'] = self.categ_id.team_id.id
            self.env['crm.claim'].create(vals)
