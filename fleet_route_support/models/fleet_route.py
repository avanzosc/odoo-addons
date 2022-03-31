# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class FleetRoute(models.Model):
    _inherit = "fleet.route"

    @api.multi
    def button_open_route_issues(self):
        self.ensure_one()
        action = self.env.ref("fleet_route_support.action_fleet_route_support")
        action_dict = action.read()[0] if action else {}
        domain = expression.AND([
            ["|", ("high_stop_route_id", "=", self.id),
             ("low_stop_route_id", "=", self.id)],
            safe_eval(action.domain or "[]")])
        action_dict.update({"domain": domain})
        return action_dict

    def route_issues(self, date=False):
        self.ensure_one()
        route_stops = self.mapped("stop_ids")
        if not date:
            date = fields.Date.context_today(self)
        issue_obj = self.env["fleet.route.support"]
        low_issues = issue_obj.search([
            ("date", "=", date),
            ("low_stop_id", "in", route_stops.ids),
        ])
        high_issues = issue_obj.search([
            ("date", "=", date),
            ("high_stop_id", "in", route_stops.ids),
        ])
        notes = issue_obj.search([
            ("type", "=", "note"),
            ("date", "=", date),
            ("student_id", "in", self.mapped("passenger_ids").ids),
        ])
        return low_issues, high_issues, notes

    def route_issue_by_type(self, type=False, date=False):
        self.ensure_one()
        if not date:
            date = fields.Date.context_today(self)
        low_issues, high_issues, notes = self.route_issues(date=date)
        if type == "low":
            return low_issues
        elif type == "high":
            return high_issues
        elif type == "notes":
            return notes
        return low_issues | high_issues | notes

    def get_route_passenger_count(self, date=False):
        self.ensure_one()
        if not date:
            date = fields.Date.context_today(self)
        low_issues, high_issues, notes = self.route_issues(date=date)
        low_partner = low_issues.mapped("student_id")
        high_partner = high_issues.mapped("student_id")
        partner_count = len(
            self.with_context(date=date).passenger_ids.filtered(
                lambda p: p not in low_partner) | high_partner)
        return partner_count

    @api.multi
    @api.depends("stop_ids", "stop_ids.passenger_ids",
                 "stop_ids.passenger_ids.start_date",
                 "stop_ids.passenger_ids.end_date",
                 "stop_ids.passenger_ids.dayofweek_ids",
                 "stop_ids.passenger_ids.partner_id")
    def _compute_passenger_ids(self):
        date = self.env.context.get("date") or fields.Date.context_today(self)
        for route in self:
            super(FleetRoute, route)._compute_passenger_ids()
            low_issues, high_issues, notes = route.route_issues(date=date)
            low_partner = low_issues.mapped("student_id")
            high_partner = high_issues.mapped("student_id")
            passenger_ids = (
                route.passenger_ids.filtered(
                    lambda p: p not in low_partner) | high_partner)
            route.passenger_ids = passenger_ids
            route.passenger_count = len(passenger_ids)
