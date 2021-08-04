# Copyright 2021 Leire Martinez de Santos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, _
from odoo.exceptions import ValidationError


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    def action_confirm(self):
        result = super(EventRegistration, self).action_confirm()
        if not self:
            return result
        for registration in self:
            user = self.env['res.users'].search([
                ('email', '=', registration.email)], limit=1)
            if not registration.partner_id:
                raise ValidationError(
                    _("The ticket reserved by is not specified!"))

            vals = {}
            if not registration.email:
                if not registration.name:
                    raise ValidationError(
                        _("You must first fill the participant data! "
                          "(Name, email...)"))
                registration.write(
                    {'email': registration.generate_user_email()})
            if user:
                partner = user.partner_id
            else:
                group_portal = self.env.ref('base.group_portal')
                use_email = registration.email
                user = registration.create_get_user({
                    'name': registration.name,
                    'email': use_email,
                    'login': use_email,
                    'groups_id': [(4, group_portal.id)]
                })
                partner = user.partner_id
                vals.update({'parent_id': registration.partner_id.id})
            if not partner:
                # Create Portal User
                partner = self.env['res.partner'].create({
                    'name': registration.name,
                    'parent_id': registration.partner_id.id
                })
                use_email = registration.email
                user = registration.create_get_user({
                    'name': registration.name,
                    'email': use_email,
                    'login': use_email,
                    'partner_id': partner.id,
                    'groups_id': [(4, group_portal.id)]
                })
            if not partner.email:
                vals.update({'email': use_email})
            if not partner.phone:
                vals.update({'phone': registration.phone})
            partner.write(vals)
            registration.student_id = partner
        return result

    def create_get_user(self, vals):
        login = vals.get('login')
        user = self.env['res.users'].search([
            ('login', '=', login)
        ])
        if not user:
            user = self.env['res.users'].create(vals)
        return user
