# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class WizEventRegistrationDraftParticipant(models.TransientModel):
    _name = 'wiz.event.registration.draft.participant'
    _description = 'Wizard for back to draft event registration participants'

    name = fields.Char(string='Description')

    def action_draft_participant(self):
        self.ensure_one()
        registrations = self.env['event.registration'].browse(
            self.env.context.get('active_ids'))
        if registrations:
            registrations = registrations.filtered(
                lambda x: x.state in ('cancel', 'done'))
            if registrations:
                registrations.action_set_draft()
