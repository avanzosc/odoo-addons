# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, _
from odoo.exceptions import UserError


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    def action_confirm(self):
        confirm_group = self.env.ref('event_registration_confirm_group.group_'
                                     'confirm_event_participants')
        if self.env.user not in confirm_group.users:
            raise UserError(
                _('The user: {} is not in the group to be able to confirm '
                  'event registrations.').format(self.env.user.name))
        public_user = self.env.ref('base.public_partner')
        for registration in self:
            if (registration.partner_id and
                    registration.partner_id == public_user):
                raise UserError(
                    _('You cannot confirm a participant with "Booked" equal '
                      'to "Public User". '))
        return super(EventRegistration, self).action_confirm()
