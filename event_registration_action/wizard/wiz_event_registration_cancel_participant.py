# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class WizEventRegistrationCancelParticipant(models.TransientModel):
    _name = 'wiz.event.registration.cancel.participant'
    _description = 'Wizard for cancel event registration participants'

    name = fields.Char(string='Description')

    def action_cancel_participant(self):
        self.ensure_one()
        registrations = self.env['event.registration'].browse(
            self.env.context.get('active_ids'))
        if registrations:
            registrations = registrations.filtered(
                lambda x: x.state in ('draft', 'open'))
            if registrations:
                registrations.action_cancel()
