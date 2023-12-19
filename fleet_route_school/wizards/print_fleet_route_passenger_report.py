# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ExportEducationRecordReport(models.TransientModel):
    _name = "print.fleet.route.passenger.report"
    _description = "Wizard to print Fleet Route Passenger Report"

    date = fields.Date(string="Select Date",
                       required=True,
                       default=lambda self: fields.Date.context_today(self))

    @api.multi
    def print_report(self):
        routes = self.env[self.env.context.get("active_model")].browse(
            self.env.context.get("active_ids"))
        [data] = self.read()
        datas = {
            "ids": self.env.context.get("active_ids"),
            "model": self.env.context.get("active_model"),
            "form": data,
        }
        return self.env.ref(
            "fleet_route_school.fleet_route_passenger_report"
        ).with_context(from_transient_model=True).report_action(
            routes, data=datas, config=False)
