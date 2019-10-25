# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class FleetRouteStop(models.Model):
    _inherit = 'fleet.route.stop'

    passenger_ids = fields.One2many(
        comodel_name='fleet.route.stop.passenger', inverse_name='stop_id',
        string='Passengers')
    going_passenger_count = fields.Integer(
        compute='_compute_passenger_count')
    coming_passenger_count = fields.Integer(
        compute='_compute_passenger_count')
    going_passenger_ids = fields.Many2many(
        comodel_name='res.partner', string='Going Passenger List',
        compute='_compute_passenger_count')
    coming_passenger_ids = fields.Many2many(
        comodel_name='res.partner', string='Coming Passenger List',
        compute='_compute_passenger_count')

    @api.multi
    @api.depends('passenger_ids', 'passenger_ids.direction')
    def _compute_passenger_count(self):
        for stop in self:
            going_passengers = stop.passenger_ids.filtered(
                lambda p: p.direction in ['going', 'round']).mapped(
                'partner_id')
            stop.going_passenger_ids = going_passengers
            stop.going_passenger_count = len(going_passengers)
            coming_passengers = stop.passenger_ids.filtered(
                lambda p: p.direction in ['coming', 'round']).mapped(
                'partner_id')
            stop.coming_passenger_ids = coming_passengers
            stop.coming_passenger_count = len(coming_passengers)
