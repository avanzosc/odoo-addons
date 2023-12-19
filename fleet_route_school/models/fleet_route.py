# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class FleetRoute(models.Model):
    _inherit = "fleet.route"

    center_ids = fields.Many2many(
        comodel_name="res.partner", string="Education Centers",
        domain=[("educational_category", "=", "school")])
    passenger_ids = fields.Many2many(
        comodel_name="res.partner", string="Passengers",
        compute="_compute_passenger_ids", compute_sudo=True)
    passenger_count = fields.Integer(
        string="Passenger Count",
        compute="_compute_passenger_ids", compute_sudo=True)

    @api.multi
    @api.depends("stop_ids", "stop_ids.passenger_ids",
                 "stop_ids.passenger_ids.start_date",
                 "stop_ids.passenger_ids.end_date",
                 "stop_ids.passenger_ids.dayofweek_ids",
                 "stop_ids.passenger_ids.partner_id")
    def _compute_passenger_ids(self):
        date = self.env.context.get("date") or fields.Date.context_today(self)
        weekday = str(date.weekday())
        for route in self:
            passengers = route.mapped(
                "stop_ids.passenger_ids").filtered(
                lambda p: ((((p.start_date and (p.start_date <= date)) or
                             not p.start_date) and
                            ((p.end_date and (p.end_date >= date)) or
                             not p.end_date)) and
                           (not p.dayofweek_ids or
                            (weekday in p.dayofweek_ids.mapped("dayofweek")))))
            passenger_ids = passengers.mapped("partner_id")
            route.passenger_ids = passenger_ids
            route.passenger_count = len(passenger_ids)
