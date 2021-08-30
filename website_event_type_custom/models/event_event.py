
from odoo import models, fields, api


class EventEvent(models.Model):
    _inherit = 'event.event'

    website_require_login = fields.Boolean(
        string="Require login for website registrations",
        default=lambda self: self.event_type_id.website_require_login)
    create_user_check = fields.Boolean(
        "Create user for attendee",
        default=lambda self: self.event_type_id.create_user_check)
    privacy_policy = fields.Html(
        string="Privacy policy",
        default=lambda self: self.event_type_id.privacy_policy)

    @api.onchange("event_type_id")
    def _onchange_event_type(self):
        for record in self:
            event_type = record.event_type_id
            record.website_require_login = event_type.website_require_login
            record.create_user_check = event_type.create_user_check
            record.privacy_policy = event_type.privacy_policy
