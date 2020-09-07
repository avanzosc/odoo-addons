# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from ..models.fleet_route_support import LOW_TYPE


class FleetRouteSupportBatchLow(models.TransientModel):
    _name = "fleet.route.support.batch.low"
    _description = "Route Low in Batch"

    partner_ids = fields.Many2many(
        comodel_name="res.partner", string="Partners")
    date = fields.Date(required=True, default=fields.Date.context_today)
    direction = fields.Selection(
        selection=[("going", "Going"),
                   ("coming", "Coming")], default="going", required=True)
    notes = fields.Text(string="Issue Description")
    low_type = fields.Selection(
        selection=LOW_TYPE, string="Low type")

    @api.model
    def default_get(self, fields):
        result = super(FleetRouteSupportBatchLow, self).default_get(fields)
        if self.env.context.get("active_ids"):
            result.update({
                "partner_ids": [
                    (6, 0, self.env.context.get("active_ids"))],
            })
        return result

    @api.multi
    def create_low_issues(self):
        issue_obj = self.env["fleet.route.support"]
        issue_vals = {
            "date": self.date,
            "type": "low",
            "notes": self.notes,
            "low_type": self.low_type,
        }
        for partner in self.partner_ids:
            stops = partner.stop_ids.filtered(
                lambda s: s.stop_id.route_id.direction == self.direction and
                ((s.start_date and (s.start_date <= self.date)) or
                    not s.start_date) and
                ((s.end_date and (s.end_date >= self.date)) or not s.end_date))
            for stop in stops:
                issue_vals.update({
                    "student_id": partner.id,
                    "low_stop_id": stop.stop_id.id,
                })
                issue_obj.create(issue_vals)
