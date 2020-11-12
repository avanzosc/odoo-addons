# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from datetime import timedelta
from odoo import api, fields, models
from ..models.fleet_route_support import LOW_TYPE


class FleetRouteSupportBatchLow(models.TransientModel):
    _name = "fleet.route.support.batch.low"
    _description = "Route Low in Batch"

    partner_ids = fields.Many2many(
        comodel_name="res.partner", string="Partners")
    date = fields.Date(required=True, default=fields.Date.context_today)
    date_end = fields.Date(
        string="Date To",
        help="If this field is not defined it will create only for the defined"
             " date")
    weekday_ids = fields.Many2many(
        comodel_name="fleet.route.stop.weekday", string="Weekdays")
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
            "type": "low",
            "notes": self.notes,
            "low_type": self.low_type,
        }
        weekday_list = [int(x) for x in self.weekday_ids.mapped("dayofweek")]
        for partner in self.partner_ids:
            date = self.date
            end_date = self.date_end or self.date
            while date <= end_date:
                if (date.weekday() in (5, 6) or
                        (weekday_list and date.weekday() not in weekday_list)):
                    date += timedelta(days=1)
                    continue
                weekday = str(date.weekday())
                stops = partner.stop_ids.filtered(
                    lambda s: s.stop_id.route_id.direction == self.direction
                    and ((((s.start_date and (s.start_date <= date)) or
                           not s.start_date) and
                          ((s.end_date and (s.end_date >= date)) or
                           not s.end_date)) and
                         (not s.dayofweek_ids or
                          (weekday in s.dayofweek_ids.mapped("dayofweek")))))
                for stop in stops:
                    issue_vals.update({
                        "date": date,
                        "student_id": partner.id,
                        "low_stop_id": stop.stop_id.id,
                    })
                    try:
                        issue_obj.create(issue_vals)
                    except Exception:
                        pass
                date += timedelta(days=1)
