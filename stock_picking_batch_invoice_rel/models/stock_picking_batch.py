# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"

    invoice_ids = fields.Many2many(
        string="Invoices",
        comodel_name="account.move",
        compute="_compute_invoice_ids",
        relation="rel_picking_batch_invoice",
        column1="picking_batch_id",
        column2="invoice_id",
        store=True,
        copy=False,
    )
    invoice_count = fields.Integer(
        string="Invoices counter", compute="_compute_invoice_count"
    )

    @api.depends("picking_ids", "picking_ids.invoice_ids")
    def _compute_invoice_ids(self):
        for batch in self:
            account_move = self.env["account.move"]
            for picking in batch.picking_ids:
                for invoice in picking.invoice_ids:
                    if invoice not in account_move:
                        account_move += invoice
            batch.invoice_ids = [(6, 0, account_move.ids)]

    def _compute_invoice_count(self):
        for batch in self:
            batch.invoice_count = len(batch.invoice_ids)

    def action_view_invoice(self):
        action = self.env.ref("account.action_move_out_invoice_type")
        action_dict = action.read()[0] if action else {}
        domain = expression.AND(
            [[("id", "in", self.invoice_ids.ids)], safe_eval(action.domain or "[]")]
        )
        action_dict.update({"domain": domain})
        return action_dict
