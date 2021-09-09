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
        compute_sudo=True)
    route_abbreviation = fields.Char(
        string='Abbreviation', related='route_id.abbreviation',
        store=True)

    @api.multi
    @api.depends("passenger_ids", "passenger_ids.partner_id",
                 "passenger_ids.start_date", "passenger_ids.end_date",
                 "passenger_ids.dayofweek_ids")
    def _compute_passenger_count(self):
        date = self.env.context.get("date", fields.Date.context_today(self))
        weekday = str(date.weekday())
        for stop in self:
            passengers = stop.mapped("passenger_ids").filtered(
                lambda p: ((((p.start_date and (p.start_date <= date)) or
                             not p.start_date) and
                            ((p.end_date and (p.end_date >= date)) or
                             not p.end_date)) and
                           (not p.dayofweek_ids or
                            (weekday in p.dayofweek_ids.mapped("dayofweek")))))
            stop.passenger_count = len(passengers.mapped("partner_id"))
