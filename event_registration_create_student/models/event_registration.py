# Copyright 2021 Leire Martinez de Santos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    create_student_user_check = fields.Boolean(
        related="event_id.create_student_user_check")
    create_student_check = fields.Boolean(
        related="event_id.create_student_check")
    generate_student_email_check = fields.Boolean(
        related="event_id.generate_student_email_check")

    @api.onchange('partner_id')
    def _onchange_reservedby(self):
        if not self.create_student_check:
            self.student_id = self.partner_id

    def action_confirm(self):
        result = super(EventRegistration, self).action_confirm()
        if not self:
            return result

        group_portal = self.env.ref('base.group_portal')
        # Action to create res.partner for student_id field
        for registration in self:
            student_user = None
            # Only create student partner if student_id is None
            if not registration.student_id:
                if registration.create_student_check:
                    attendee_user = None
                    if not registration.partner_id:
                        raise ValidationError(
                            _("The ticket reserved by is not specified!"))

                    if not registration.name:
                        raise ValidationError(
                            _("You must first fill the participant data! "
                              "(Name, email...)"))
                    else:
                        # Check if user already exists with the set email field in
                        # event.registration
                        attendee_user = self.create_get_user({
                            'login': registration.email}, False)

                    reserved_by = registration.partner_id

                    if attendee_user and attendee_user.partner_id == reserved_by:
                        raise ValidationError(
                            _("Notice that you are confirming an attendee that  "
                              "coincides with the Reserved by partner email."))

                    student_user = attendee_user
                    student_partner = attendee_user.partner_id if \
                        student_user else None

                    if not student_partner:
                        # Create res.partner for event.registration Student
                        student_partner = self.env['res.partner'].create({
                            'name': registration.name,
                            'email': registration.email,
                            'phone': registration.phone,
                            'mobile': registration.mobile,
                            'parent_id': reserved_by.id
                        })

                else:
                    student_partner = registration.partner_id

                registration.write({
                  'student_id': student_partner.id})
            else:
                student_partner = registration.student_id
                student_user = student_partner.user_id

            if student_partner and registration.generate_student_email_check \
                    and not student_partner.email:
                # If event.registration email is not set, generate one
                student_partner.write({
                    'email': registration.generate_user_email()})

            if not student_user and registration.create_student_user_check:
                if not student_partner.email:
                    if not registration.email:
                        raise ValidationError(
                            _("You must set/generate an email for the attendee"
                              " in order to create a portal user!"))
                    # If partner does not have an email, use the one from
                    # event.register
                    student_partner.write({'email': registration.email})

                # If student partner does not have Portal User, create one
                student_user = registration.create_get_user({
                    'name': registration.name,
                    'email': student_partner.email,
                    'login': student_partner.email,
                    'partner_id': student_partner.id,
                    'groups_id': [(4, group_portal.id)]
                })

        return result

    def create_get_user(self, vals, create=True):
        login = vals.get('login')
        user = self.env['res.users'].search([
                    ('login', '=', login)], limit=1)
        if not user and create:
            user = self.env['res.users'].create(vals)
        return user
