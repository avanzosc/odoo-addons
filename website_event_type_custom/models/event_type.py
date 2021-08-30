
from odoo import models, fields, api


class EventType(models.Model):
    _inherit = 'event.type'

    website_require_login = fields.Boolean(
        string="Require login for website registrations")
    create_user_check = fields.Boolean(string="Create user for attendee")
    privacy_policy = fields.Html(string="Privacy policy")
