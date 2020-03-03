# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class FleetRouteStopWeekday(models.Model):
    _name = "fleet.route.stop.weekday"
    _description = "Route Stop Weekday"

    @api.model
    def _get_selection_dayofweek(self):
        return self.env["resource.calendar.attendance"].fields_get(
            allfields=["dayofweek"])["dayofweek"]["selection"]

    def default_dayofweek(self):
        default_dict = self.env["resource.calendar.attendance"].default_get([
            "dayofweek"])
        return default_dict.get("dayofweek")

    name = fields.Char(string="Weekday", required=True, translate=True)
    dayofweek = fields.Selection(
        selection="_get_selection_dayofweek", string="Day of Week",
        required=True, index=True, default=default_dayofweek)
