# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class WizEventRegistrationConfirmSaleOrder(models.TransientModel):
    _name = 'wiz.event.registration.confirm.sale.order'
    _description = 'Wizard for confirm sales order from event registration'

    name = fields.Char(string='Description')

    def action_confirm_sale_order(self):
        self.ensure_one()
        registrations = self.env['event.registration'].browse(
            self.env.context.get('active_ids'))
        if registrations:
            for registration in registrations.filtered(
                lambda x: x.sale_order_id and
                    x.sale_order_id.state in ('draft', 'sent')):
                registration.sale_order_id.action_confirm()
