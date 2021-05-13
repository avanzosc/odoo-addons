# Copyright 2021 Leire Martinez de Santos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    def action_confirm(self):
        super(EventRegistration, self).action_confirm()
        user = self.env['res.users'].search([
            ('email', '=', self.email)
        ], limit=1)

        if user:
            partner = user.partner_id
        else:
            partner = self.env['res.partner'].search([
                ('parent_id', '=', self.partner_id.id),
                ('email', '=', self.email)
            ], limit=1)

        if not partner:
            # Create Portal User
            partner = self.env['res.partner'].create({
                'name': self.name,
                'parent_id': self.partner_id.id
            })

        vals = {}
        if not partner.email:
            vals.update({'email': self.email})
        if not partner.phone:
            vals.update({'phone': self.phone})

        partner.write(vals)
        self.student_id = partner
