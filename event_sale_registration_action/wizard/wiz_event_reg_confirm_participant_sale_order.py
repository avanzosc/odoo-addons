# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class WizEventRegConfirmParticipantSaleOrder(models.TransientModel):
    _name = 'wiz.event.reg.confirm.participant.sale.order'
    _description = 'Wizard for confirm participants and sales orders'

    name = fields.Char(string='Description')

    def action_confirm_participant_sale_order(self):
        self.ensure_one()
        registrations = self.env['event.registration'].browse(
            self.env.context.get('active_ids'))
        if registrations:
            for registration in registrations:
                if registration.state == 'draft':
                    registrations.action_confirm()
                if (registration.sale_order_id and
                        registration.sale_order_id.state in ('draft', 'sent')):
                    registration.sale_order_id.action_confirm()
