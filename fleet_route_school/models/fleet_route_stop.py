# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class FleetRouteStop(models.Model):
    _inherit = 'fleet.route.stop'

    passenger_ids = fields.One2many(
        comodel_name='fleet.route.stop.passenger', inverse_name='stop_id',
        string='Passengers')
    passenger_count = fields.Integer(
        string="Passenger Count", compute='_compute_passenger_count',
        store=True)
    route_abbreviation = fields.Char(
        string='Abbreviation', related='route_id.abbreviation',
        store=True)

    @api.multi
    @api.depends("passenger_ids", "passenger_ids.partner_id")
    def _compute_passenger_count(self):
        for stop in self:
            stop.passenger_count = len(stop.mapped("passenger_ids.partner_id"))
