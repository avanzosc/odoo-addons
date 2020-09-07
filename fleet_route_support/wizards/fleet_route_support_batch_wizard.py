# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from ..models.fleet_route_support import ISSUE_TYPE, LOW_TYPE


class FleetRouteSupportBatchWizard(models.TransientModel):
    _name = "fleet.route.support.batch.wizard"
    _description = "Wizard to create route issues in Batch"

    passenger_ids = fields.Many2many(
        comodel_name="fleet.route.stop.passenger", name="Passengers")
    date = fields.Date(required=True, default=fields.Date.context_today)
    type = fields.Selection(
        selection=ISSUE_TYPE, string="Type",
        required=True)
    high_stop_id = fields.Many2one(
        comodel_name="fleet.route.stop", string="High stop")
    notes = fields.Text(string="Issue Description")
    low_type = fields.Selection(
        selection=LOW_TYPE, string="Low type")

    @api.model
    def default_get(self, fields):
        result = super(FleetRouteSupportBatchWizard, self).default_get(fields)
        if self.env.context.get("active_ids"):
            result.update({
                "passenger_ids": [
                    (6, 0, self.env.context.get("active_ids"))],
            })
        return result

    @api.multi
    def create_issues(self):
        issue_obj = self.env["fleet.route.support"]
        issue_vals = {
            "date": self.date,
            "type": self.type,
            "notes": self.notes,
            "low_type": self.low_type,
        }
        if self.type in ('high', 'change'):
            issue_vals.update({
                "high_stop_id": self.high_stop_id.id,
            })
        for passenger in self.passenger_ids:
            issue_vals.update({
                "student_id": passenger.partner_id.id,
                "low_stop_id": passenger.stop_id.id,
            })
            issue_obj.create(issue_vals)
