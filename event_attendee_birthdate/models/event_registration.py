# Copyright 2021 Leire Martinez de Santos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    birthdate = fields.Date('Attendee birthdate')
    age = fields.Integer('Attendee age', compute="_compute_attendee_age")

    @api.depends('birthdate')
    def _compute_attendee_age(self):
        for res in self:
            age = 0
            if res.birthdate:
                age = relativedelta(fields.Date.today(), res.birthdate).years
            res.age = age

    def _get_website_registration_allowed_fields(self):
        res = super(EventRegistration,
                    self)._get_website_registration_allowed_fields()
        res.update({'birthdate'})
        return res
