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
        compute="_compute_passenger_ids", compute_sudo=True, store=True)

    @api.multi
    @api.depends("stop_ids", "stop_ids.passenger_ids",
                 "stop_ids.passenger_ids.partner_id")
    def _compute_passenger_ids(self):
        for route in self:
            passenger_ids = route.mapped(
                "stop_ids.passenger_ids.partner_id")
            route.passenger_ids = passenger_ids
            route.passenger_count = len(passenger_ids)
