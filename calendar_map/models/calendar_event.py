from odoo import fields, models


class CalendarEvent(models.Model):
    _inherit = "calendar.event"

    visit_address_id = fields.Many2one(
        "res.partner",
        string="Visit Address",
        help="Select the partner for the visit address.",
    )
