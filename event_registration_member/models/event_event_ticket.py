
from odoo import models, fields


class EventEventTicket(models.Model):
    _inherit = 'event.event.ticket'

    is_member = fields.Boolean(string='Is member?', default=False)


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    is_member = fields.Boolean(string='Is member?', default=False)
