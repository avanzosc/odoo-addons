# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class AccountMove(models.Model):
    _inherit = "account.move"

    invoice_origin = fields.Char(readonly=False)
    count_stock_valuation_layer = fields.Integer(
        string="Num. Stock Valuation Layer",
        compute="_compute_count_stock_valuation_layer",
        store=True,
        copy=False,
    )

    @api.depends("line_ids", "line_ids.stock_valuation_layer_ids")
    def _compute_count_stock_valuation_layer(self):
        for invoice in self:
            invoice.count_stock_valuation_layer = len(
                invoice.line_ids.mapped("stock_valuation_layer_ids")
            )

    def action_view_stock_valuation_layer(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "stock_account.stock_valuation_layer_action"
        )
        action["domain"] = expression.AND(
            [
                [("id", "=", self.line_ids.mapped("stock_valuation_layer_ids").ids)],
                safe_eval(action.get("domain") or "[]"),
            ]
        )
        return action
