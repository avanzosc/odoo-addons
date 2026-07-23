# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from odoo.osv import expression
from odoo.tools.safe_eval import safe_eval


class StockLocation(models.Model):
    _inherit = "stock.location"

    has_children = fields.Boolean(compute="_compute_has_children", store=True)
    num_children = fields.Integer(
        string="Num. Children", compute="_compute_has_children", store=True
    )

    @api.depends("child_ids")
    def _compute_has_children(self):
        for location in self:
            children = location.child_internal_location_ids - location
            location.has_children = bool(children)
            location.num_children = len(children)

    def action_view_location_children(self):
        self.ensure_one()
        children = self.child_internal_location_ids - self
        action = self.env["ir.actions.actions"]._for_xml_id(
            "stock.action_location_form"
        )
        action["domain"] = expression.AND(
            [
                [("id", "in", children.ids)],
                safe_eval(action.get("domain") or "[]"),
            ]
        )
        return action
