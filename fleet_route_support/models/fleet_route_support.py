# Copyright (c) 2019 Adrian Revilla <adrianrevilla@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class FleetRouteSupport(models.Model):
    _name = "fleet.route.support"
    _description = "Fleet route support"

    date = fields.Date(string="Date", required=True,
                       index=True, copy=False,
                       default=fields.Date.context_today)
    student_id = fields.Many2one(
        comodel_name="res.partner", string="Student",
        domain="[('educational_category', '=', 'student')]",
        required=True)
    type = fields.Selection(
        selection=[("high", "High"),
                   ("low", "Low"),
                   ("change", "Change"),
                   ("note", "Note")], string="Type",
        required=True)
    high_stop_id = fields.Many2one(
        comodel_name="fleet.route.stop.passenger", string="High stop",
        domain="[('partner_id', '=', student_id)]")
    high_stop_route_id = fields.Many2one(
        related="high_stop_id.route_id", comodel_name="fleet.route",
        string="High stop route")
    high_stop_direction = fields.Selection(
        related="high_stop_route_id.direction", string="High stop direction")
    low_stop_id = fields.Many2one(
        comodel_name="fleet.route.stop.passenger", string="Low stop",
        domain="[('partner_id', '=', student_id)]")
    low_stop_route_id = fields.Many2one(
        related="low_stop_id.route_id", comodel_name="fleet.route",
        string="Low stop route")
    low_stop_direction = fields.Selection(
        related="low_stop_route_id.direction", string="Low stop direction")
    notes = fields.Text(string="Incidence description")
    low_type = fields.Selection(
        selection=[("lack of assistance", "Lack of assistance"),
                   ("pick-up notice", "Pick-up notice")],
        string="Low type")
