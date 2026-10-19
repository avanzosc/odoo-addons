# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.depends("matching_number")
    def _compute_matching_line_ids(self):
        for line in self:
            if line.matching_number:
                line.matching_line_ids = self.search(
                    [("matching_number", "=", line.matching_number)]
                )
            else:
                line.matching_line_ids = self.env["account.move.line"]

    matching_line_ids = fields.One2many(
        comodel_name="account.move.line",
        compute="_compute_matching_line_ids",
        string="Reconciled lines",
    )

    def action_open_matching_lines(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "account.action_account_moves_all"
        )
        domain = expression.AND(
            [
                [("matching_number", "=", self.matching_number)],
                safe_eval(action.get("domain") or "[]"),
            ]
        )
        context = safe_eval(action.get("context") or "{}")
        context.update(
            {
                "matching_lines": True,
            }
        )
        action.update(
            {
                "domain": domain,
                "context": context,
            }
        )
        return action
