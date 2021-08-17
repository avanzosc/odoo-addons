# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class WizEventRegistrationConfirmParticipant(models.TransientModel):
    _name = 'wiz.event.registration.confirm.participant'
    _description = 'Wizard for confirm event registration participants'

    name = fields.Char(string='Description')

    def action_confirm_participant(self):
        self.ensure_one()
        registrations = self.env['event.registration'].browse(
            self.env.context.get('active_ids'))
        if registrations:
            registrations = registrations.filtered(
                lambda x: x.state == 'draft')
            if registrations:
                registrations.action_confirm()
