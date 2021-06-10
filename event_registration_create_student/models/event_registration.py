# Copyright 2021 Leire Martinez de Santos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    def action_confirm(self):
        super(EventRegistration, self).action_confirm()
        user = self.env['res.users'].search([
            ('email', '=', self.email)
        ], limit=1)

        vals = {}
        if user:
            partner = user.partner_id
        else:
            group_portal = self.env.ref('base.group_portal')
            user = self.create_get_user({
                'name': self.name,
                'email': self.email,
                'login': self.email,
                'groups_id': [(4, group_portal.id)]
            })
            partner = user.partner_id
            vals.update({'parent_id': self.partner_id.id})

        if not partner:
            # Create Portal User
            partner = self.env['res.partner'].create({
                'name': self.name,
                'parent_id': self.partner_id.id
            })
            user = self.create_get_user({
                'name': self.name,
                'email': self.email,
                'login': self.email,
                'partner_id': partner.id,
                'groups_id': [(4, group_portal.id)]
            })

        if not partner.email:
            vals.update({'email': self.email})
        if not partner.phone:
            vals.update({'phone': self.phone})

        partner.write(vals)
        self.student_id = partner

    def create_get_user(self, vals):
        login = vals.get('login')
        user = self.env['res.users'].search([
            ('login', '=', login)
        ])
        if not user:
            user = self.env['res.users'].create(vals)
        return user
