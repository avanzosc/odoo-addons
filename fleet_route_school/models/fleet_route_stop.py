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

    @api.multi
    @api.depends('passenger_ids', 'passenger_ids.direction')
    def _compute_passenger_count(self):
        for stop in self:
            stop.going_passenger_count = len(stop.passenger_ids.filtered(
                lambda p: p.direction in ['going', 'round']))
            stop.coming_passenger_count = len(stop.passenger_ids.filtered(
                lambda p: p.direction in ['coming', 'round']))
