# Copyright 2020 Adrian Revilla - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class FleetRoute(models.Model):
    _inherit = 'fleet.route'

    @api.multi
    def _get_report_fleet_base_filename(self):
        self.ensure_one()
        return self.display_name

    def _get_actual_date(self):
        self.ensure_one()
        return fields.Date.context_today(self).strftime('%Y-%m-%d')

    def current_issues(self):
        self.ensure_one()
        route_stops = self.mapped("stop_ids")
        today = fields.Date.context_today(self)
        issue_obj = self.env["fleet.route.support"]
        low_issues = issue_obj.search([
            ("date", "=", today),
            ("low_stop_id", "in", route_stops.ids),
        ])
        high_issues = issue_obj.search([
            ("date", "=", today),
            ("high_stop_id", "in", route_stops.ids),
        ])
        notes = issue_obj.search([
            ("type", "=", "note"),
            ("date", "=", today),
            ("student_id", "in", self.mapped("passenger_ids").ids),
        ])
        return low_issues, high_issues, notes

    def current_issue_by_type(self, type=False):
        if not type:
            return
        low_issues, high_issues, notes = self.current_issues()
        if type == "low":
            return low_issues
        elif type == "high":
            return high_issues
        elif type == "notes":
            return notes
        return low_issues | high_issues | notes
