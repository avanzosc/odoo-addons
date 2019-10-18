# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class FleetRouteStopPassenger(models.Model):
    _name = 'fleet.route.stop.passenger'
    _description = 'Passenger'

    partner_id = fields.Many2one(
        comodel_name='res.partner', string='Passenger', required=True)
    stop_id = fields.Many2one(
        comodel_name='fleet.route.stop', string='Route Stop', required=True)
    start_date = fields.Date()
    end_date = fields.Date()
    direction = fields.Selection(
        selection=[('round', 'Round Trip'),
                   ('going', 'Going'),
                   ('coming', 'Coming')], default='round', required=True)
    notes = fields.Text()
