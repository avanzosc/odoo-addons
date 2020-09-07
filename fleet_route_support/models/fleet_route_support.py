# Copyright (c) 2019 Adrian Revilla <adrianrevilla@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

ISSUE_TYPE = [("high", "High"),
              ("low", "Low"),
              ("change", "Change"),
              ("note", "Note")]
LOW_TYPE = [("lack of assistance", "Lack of assistance"),
            ("pick-up notice", "Pick-up notice")]


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
        selection=ISSUE_TYPE, string="Type",
        required=True)
    high_stop_id = fields.Many2one(
        comodel_name="fleet.route.stop", string="High stop")
    high_stop_route_id = fields.Many2one(
        related="high_stop_id.route_id", comodel_name="fleet.route",
        string="High stop route")
    high_stop_direction = fields.Selection(
        related="high_stop_route_id.direction", string="High stop direction")
    low_stop_id = fields.Many2one(
        comodel_name="fleet.route.stop", string="Low stop")
    low_stop_route_id = fields.Many2one(
        related="low_stop_id.route_id", comodel_name="fleet.route",
        string="Low stop route")
    low_stop_direction = fields.Selection(
        related="low_stop_route_id.direction", string="Low stop direction")
    notes = fields.Text(string="Incidence description")
    low_type = fields.Selection(
        selection=LOW_TYPE, string="Low type")

    @api.onchange('date', 'student_id')
    def _getPassengerStopDomain(self):
        passenger_stop_ids = self.env["fleet.route.stop.passenger"].search(
            ['&', '|', ("start_date", "<", self.date),
             ("start_date", "=", False),
             '|', ("end_date", ">", self.date),
             ("end_date", "=", False)])
        stop_ids = []
        for passenger_stop in passenger_stop_ids.filtered(
                lambda p: p.partner_id.id == self.student_id.id):
            stop_ids.append(passenger_stop.stop_id.id)
        res = {}
        res['domain'] = {'low_stop_id': [('id', 'in', stop_ids)]}
        return res
