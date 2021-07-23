# Copyright 2021 Leire Martinez de Santos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, _
from odoo.exceptions import ValidationError


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    def action_confirm(self):
        super(EventRegistration, self).action_confirm()
        if not self:
            return

        user = self.env['res.users'].search([
            ('email', '=', self.email)
        ], limit=1)

        if not self.partner_id:
            raise ValidationError(
                _("The ticket reserved by is not specified!"))

        vals = {}
        if not self.email:
            if not self.name:
                raise ValidationError(
                    _("You must first fill the participant data! "
                      "(Name, email...)"))

            self.write({'email': self.generate_user_email()})

        if user:
            partner = user.partner_id
        else:
            group_portal = self.env.ref('base.group_portal')
            use_email = self.email
            user = self.create_get_user({
                'name': self.name,
                'email': use_email,
                'login': use_email,
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
            use_email = self.email
            user = self.create_get_user({
                'name': self.name,
                'email': use_email,
                'login': use_email,
                'partner_id': partner.id,
                'groups_id': [(4, group_portal.id)]
            })

        if not partner.email:
            vals.update({'email': use_email})
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
