
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    participant_birthdate = fields.Date('Participant birthdate')
    participant_age = fields.Integer('Participant age',
                                     compute="_compute_partner_age")

    @api.depends('participant_birthdate')
    def _compute_partner_age(self):
        for res in self:
            age = 0
            if res.participant_birthdate:
                age = relativedelta(fields.Date.today(),
                                    res.participant_birthdate).years
            res.participant_age = age

    def _get_website_registration_allowed_fields(self):
        res = super(EventRegistration,
                    self)._get_website_registration_allowed_fields()
        res.update({'participant_birthdate'})
        return res
