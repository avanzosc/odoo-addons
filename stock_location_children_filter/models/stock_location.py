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
    num_descendants = fields.Integer(
        string="Num. Descendants", compute="_compute_num_descendants", store=True
    )

    @api.depends("child_ids")
    def _compute_has_children(self):
        for location in self:
            location.has_children = bool(location.child_ids)
            location.num_children = len(location.child_ids)

    @api.depends("child_ids", "child_ids.num_descendants")
    def _compute_num_descendants(self):
        for location in self:
            location.num_descendants = len(location.child_ids) + sum(
                location.child_ids.mapped("num_descendants")
            )

    def action_view_location_children(self):
        self.ensure_one()
        children = self.child_ids
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
