# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class FleetRoute(models.Model):
    _inherit = "fleet.route"

    @api.multi
    def button_open_route_issues(self):
        self.ensure_one()
        action = self.env.ref("fleet_route_support.action_fleet_route_support")
        action_dict = action.read()[0] if action else {}
        domain = expression.AND([
            ["|", ("high_stop_route_id", "=", self.id),
             ("low_stop_route_id", "=", self.id)],
            safe_eval(action.domain or "[]")])
        action_dict.update({"domain": domain})
        return action_dict
