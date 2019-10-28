# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


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
    departure_estimated_time = fields.Float(
        string='Departure estimated time',
        compute='_compute_scheduled_time', store=True)
    return_estimated_time = fields.Float(
        string='Return estimated time', compute='_compute_scheduled_time',
        store=True)
    route_id = fields.Many2one(
        comodel_name='fleet.route', related='stop_id.route_id',
        string='Route', store=True)
    route_abbreviation = fields.Char(
        string='Abbreviation', related='stop_id.route_id.abbreviation',
        store=True)
    manager_id = fields.Many2one(
        string='Manager', comodel_name='hr.employee',
        related='stop_id.route_id.manager_id', store=True)
    manager_phone_mobile = fields.Char(
        string='Phone/mobile',
        related='stop_id.route_id.manager_phone_mobile', store=True)

    @api.depends('stop_id', 'direction', 'stop_id.departure_estimated_time',
                 'stop_id.return_estimated_time')
    def _compute_scheduled_time(self):
        for passenger in self:
            passenger.departure_estimated_time = (
                passenger.stop_id.departure_estimated_time if
                passenger.direction in ['round', 'going'] else 0.0)
            passenger.return_estimated_time = (
                passenger.stop_id.return_estimated_time if
                passenger.direction in ['round', 'coming'] else 0.0)
