
from odoo import models, fields, api


class EventEvent(models.Model):
    _inherit = 'event.event'

    create_user_check = fields.Boolean("Create user for attendee")
