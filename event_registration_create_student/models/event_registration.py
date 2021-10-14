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

    @api.onchange('student_id', "partner_id")
    def _onchange_student_id(self):
        super(EventRegistration, self)._onchange_student_id()
        if self.student_id and not self.student_id.email:
            if self.email == self.partner_id.email:
                self.email = self.student_id.email
            if self.phone == self.partner_id.phone:
                self.phone = self.student_id.phone
            if self.mobile == self.partner_id.mobile:
                self.mobile = self.student_id.mobile

    def action_confirm(self):
        result = super(EventRegistration, self).action_confirm()
        if not self:
            return result
        self.create_registration_student()
        return result

    def create_registration_student(self):
        # Action to create res.partner for student_id field
        for registration in self:
            student_user = None
            # Only create student partner if student_id is None
            if not registration.student_id:
                student_partner = registration.action_create_student_partner()

            else:
                student_partner = registration.student_id
                student_user = student_partner.user_id

            if student_partner and registration.generate_student_email_check \
                    and not student_partner.email:
                registration.action_generate_student_email(student_partner)

            if not student_user and registration.create_student_user_check:
                student_user = registration.action_create_student_user(
                    student_partner)

        return True

    def action_create_student_partner(self, force_create=False):
        if not self.partner_id:
            raise ValidationError(
                _("The ticket reserved by is not specified!"))

        booked_by = self.partner_id
        if not force_create and not self.create_student_check:
            # If check 'create_student_check' not clicked, set Booked by as
            # student
            student_partner = booked_by
        else:
            if not self.name:
                raise ValidationError(
                    _("You must first fill the participant data! "
                      "(Name, email...)"))

            if not force_create:
                # Check if user already exists with the set email field in
                # event.registration
                attendee_user = self.create_get_user({
                    'login': self.email}, False)

                if attendee_user and attendee_user.partner_id == booked_by:
                    raise ValidationError(
                        _("Notice that you are confirming an attendee that  "
                          "coincides with the Reserved by partner email."))

                student_user = attendee_user
                student_partner = attendee_user.partner_id if \
                    student_user else None
            else:
                student_partner = None

            if not student_partner:
                # Create res.partner for event.registration Student
                student_partner = self.env['res.partner'].create({
                    'name': self.name,
                    'email': self.email,
                    'phone': self.phone,
                    'mobile': self.mobile,
                    'parent_id': booked_by.id
                })

        self.write({
            'student_id': student_partner.id})
        return student_partner

    def action_create_student_user(self, student_partner=None):

        if not student_partner:
            if not self.student_id:
                return None
            student_partner = self.student_id

        group_portal = self.env.ref('base.group_portal')
        if not student_partner.email:
            if not self.email:
                raise ValidationError(
                    _("You must set/generate an email for the attendee"
                      " in order to create a portal user!"))
            # If partner does not have an email, use the one from
            # event.register
            student_partner.write({'email': self.email})

        # If student partner does not have Portal User, create one
        student_user = self.create_get_user({
            'name': self.name,
            'email': student_partner.email,
            'login': student_partner.email,
            'partner_id': student_partner.id,
            'groups_id': [(4, group_portal.id)]
        })

        return student_user

    def action_generate_student_email(self, student_partner):
        # If event.registration email is not set, generate one
        student_email = self.generate_user_email()
        student_partner.write({
            'email': student_email})
        self.write({
            'email': student_email})

    def create_get_user(self, vals, create=True):
        login = vals.get('login')
        user = self.env['res.users'].search([
                    ('login', '=', login)], limit=1)
        if not user and create:
            user = self.env['res.users'].create(vals)
        return user

    def create_student_user(self):
        for record in self:
            record.action_create_student_user(record.student_id and record.student_id)
