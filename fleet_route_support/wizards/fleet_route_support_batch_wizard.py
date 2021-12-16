# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from datetime import timedelta
from odoo import api, fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval
from ..models.fleet_route_support import ISSUE_TYPE, LOW_TYPE


class FleetRouteSupportBatchWizard(models.TransientModel):
    _name = "fleet.route.support.batch.wizard"
    _description = "Wizard to create route issues in Batch"

    passenger_ids = fields.Many2many(
        comodel_name="fleet.route.stop.passenger", name="Passengers")
    partner_ids = fields.Many2many(
        comodel_name="res.partner", string="Partners")
    date = fields.Date(required=True, default=fields.Date.context_today)
    date_end = fields.Date(
        string="Date To",
        help="If this field is not defined it will create only for the defined"
             " date")
    weekday_ids = fields.Many2many(
        comodel_name="fleet.route.stop.weekday", string="Weekdays")
    type = fields.Selection(
        selection=ISSUE_TYPE, string="Type",
        required=True)
    high_stop_id = fields.Many2one(
        comodel_name="fleet.route.stop", string="High stop")
    notes = fields.Text(string="Issue Description")
    direction = fields.Selection(
        selection=[("going", "Going"),
                   ("coming", "Coming"),
                   ("both", "Both")],
        string="Direction",
        default="both")
    low_type = fields.Selection(
        selection=LOW_TYPE, string="Low type")

    @api.model
    def default_get(self, fields):
        result = super(FleetRouteSupportBatchWizard, self).default_get(fields)
        if self.env.context.get("active_ids"):
            active_model = self.env.context.get("active_model")
            if active_model == "fleet.route.stop.passenger":
                result.update({
                    "passenger_ids": [
                        (6, 0, self.env.context.get("active_ids"))],
                })
            elif active_model == "res.partner":
                result.update({
                    "partner_ids": [
                        (6, 0, self.env.context.get("active_ids"))],
                })
        return result

    @api.multi
    def create_issues(self):
        issue_obj = self.env["fleet.route.support"]
        issue_vals = {
            "type": self.type,
            "notes": self.notes,
            "low_type": self.low_type,
        }
        if self.type in ('high', 'change'):
            issue_vals.update({
                "high_stop_id": self.high_stop_id.id,
            })
        date = self.date
        end_date = self.date_end or self.date
        weekday_list = [int(x) for x in self.weekday_ids.mapped("dayofweek")]
        direction = False if self.direction == "both" else self.direction
        while date <= end_date:
            if (date.weekday() in (5, 6) or
                    (weekday_list and date.weekday() not in weekday_list)):
                date += timedelta(days=1)
                continue
            weekday = str(date.weekday())
            issue_vals.update({
                "date": date,
            })
            for passenger in self.passenger_ids.filtered(
                    lambda p: ((((p.start_date and (p.start_date <= date)) or
                                 not p.start_date) and
                                ((p.end_date and (p.end_date >= date)) or
                                 not p.end_date)) and
                               (not p.dayofweek_ids or
                                (weekday in p.dayofweek_ids.mapped("dayofweek"))))):
                issue_vals.update({
                    "student_id": passenger.partner_id.id,
                    "low_stop_id": passenger.stop_id.id,
                })
                if (issue_vals.get("type") == "change" and
                        self.high_stop_id.route_id.direction !=
                        passenger.stop_id.direction):
                    continue
                try:
                    issue_obj.create(issue_vals)
                except Exception:
                    pass
            for partner in self.partner_ids:
                issue_vals.update({
                    "student_id": partner.id,
                })
                stops = partner.stop_ids.filtered(
                    lambda s: ((((s.start_date and (s.start_date <= date)) or
                                 not s.start_date) and
                                ((s.end_date and (s.end_date >= date)) or
                                 not s.end_date)) and
                               (not s.dayofweek_ids or
                                (weekday in s.dayofweek_ids.mapped("dayofweek")))))
                if self.type == "high":
                    if not stops:
                        issue_obj.create(issue_vals)
                        continue
                    else:
                        issue_vals.update({
                            "type": "change",
                        })
                elif self.type in ("low", "note") and direction:
                    stops = stops.filtered(
                        lambda s: s.stop_id.route_id.direction == direction)
                for stop in stops:
                    issue_vals.update({
                        "low_stop_id": stop.stop_id.id,
                    })
                    if ((issue_vals.get("type") == "change" and
                            self.high_stop_id.route_id.direction !=
                            stop.stop_id.direction)):
                        continue
                    try:
                        issue_obj.create(issue_vals)
                    except Exception:
                        pass
            date += timedelta(days=1)
        action = self.env.ref("fleet_route_support.action_fleet_route_support")
        action_dict = action and action.read()[0]
        domain = expression.AND([
            [("date", "<=", self.date), ("date", ">=", end_date)],
            safe_eval(action.domain or '[]')
        ])
        context = safe_eval(action.context or '{}')
        context.update({
            "search_default_today": 0,
        })
        action_dict.update({
            "domain": domain,
            "context": context,
        })
        return action_dict
