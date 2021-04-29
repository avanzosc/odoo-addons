
from odoo import api, fields, models


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    participant_birthdate = fields.Date('Participant birthdate')
    participant_age = fields.Integer('Participant age',
                                     compute="_compute_partner_age")

    @api.depends('participant_birthdate')
    def _compute_partner_age(self):
        today = fields.Date.today()
        for res in self:
            if res.participant_birthdate:
                res.participant_age = today.year - res.participant_birthdate.year
            else:
                res.participant_age = None

    def _get_website_registration_allowed_fields(self):
        res = super(EventRegistration, self)._get_website_registration_allowed_fields()
        res.update({'participant_birthdate'})
        return res
