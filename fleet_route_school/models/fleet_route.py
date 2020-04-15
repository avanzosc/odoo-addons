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
        compute="_compute_passenger_ids")

    @api.multi
    @api.depends("stop_ids")
    def _compute_passenger_ids(self):
        for route in self:
            route.passenger_ids = route.mapped(
                "stop_ids.passenger_ids.partner_id")
