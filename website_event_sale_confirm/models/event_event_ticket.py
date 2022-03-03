
from odoo import fields, models


class EventEventTicket(models.Model):
    _inherit = 'event.event.ticket'

    confirm_free_ticket = fields.Boolean(
        string='Confirm free ticket', default=False)
