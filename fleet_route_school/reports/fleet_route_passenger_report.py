# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class FleetRoutePassengerReport(models.AbstractModel):
    _name = "report.fleet_route_school.fleet_route_passenger_report_qweb"
    _description = "Fleet Route Passenger Report"

    @api.model
    def _get_report_values(self, docids, data=None):
        if not data.get("form"):
            raise UserError(
                _("Form content is missing, this report cannot be printed."))
        passenger_report = self.env["ir.actions.report"]._get_report_from_name(
            "fleet_route_school.fleet_route_passenger_report")
        routes = self.env["fleet.route"].browse(data["ids"])
        return {
            "doc_ids": data["ids"],
            "doc_model": passenger_report.model,
            "docs": routes,
            "selected_date": fields.Date.from_string(data["form"]["date"]),
        }
