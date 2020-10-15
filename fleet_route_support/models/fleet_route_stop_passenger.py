# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class FleetRoutePassenger(models.Model):
    _inherit = "fleet.route.stop.passenger"

    def check_low_or_change_issue(self, date=False):
        self.ensure_one()
        if not date:
            date = fields.Date.context_today(self)
        issues = self.env["fleet.route.support"].search([
            ("date", "=", date),
            ("type", "in", ["low", "change"]),
            ("low_stop_id", "=", self.stop_id.id),
            ("student_id", "=", self.partner_id.id),
        ])
        if issues:
            return True
        return False
