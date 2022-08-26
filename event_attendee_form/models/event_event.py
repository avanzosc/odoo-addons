# Copyright 2022 Leire Martinez de Santos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class EventEvent(models.Model):
    _inherit = 'event.event'

    canteen_or_spend_night = fields.Boolean(
        'Offer dinning or spending the night')

