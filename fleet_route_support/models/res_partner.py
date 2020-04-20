# Copyright (c) 2019 Adrian Revilla <adrianrevilla@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class ResPartnerBusIssues(models.Model):
    _inherit = "res.partner"

    bus_issue_ids = fields.One2many(
        string="Bus Issues", comodel_name="fleet.route.support",
        inverse_name="student_id")
    bus_issue_count = fields.Integer(
        string="Bus Issue Count", compute="_compute_bus_issue_count")

    @api.multi
    @api.depends("bus_issue_ids")
    def _compute_bus_issue_count(self):
        for partner in self:
            partner.bus_issue_count = len(partner.bus_issue_ids)

    @api.multi
    def button_bus_issues(self):
        self.ensure_one()
        action = self.env.ref("fleet_route_support.action_fleet_route_support")
        action_dict = action.read()[0] if action else {}
        action_dict["context"] = safe_eval(
            action_dict.get("context", "{}"))
        action_dict["context"].update({
            "default_student_id": self.id,
        })
        domain = expression.AND([
            [("student_id", "in", self.ids)],
            safe_eval(action.domain or "[]")])
        action_dict.update({"domain": domain})
        return action_dict
