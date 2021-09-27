# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class SlideChannelPartner(models.Model):
    _inherit = "slide.channel.partner"

    event_registration_id = fields.Many2one(
        string='Event registration', comodel_name='event.registration')
    real_date_start = fields.Date(
        string='Real date start')
    real_date_end = fields.Date(
        string='Real date end')
    birthdate = fields.Date(
        string='Attendee birthdate', related='event_registration_id.birthdate',
        store=True)
    age = fields.Integer(
        string='Attendee age', related='event_registration_id.age')
