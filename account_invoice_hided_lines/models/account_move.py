# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    invoice_with_produt_lines = fields.Boolean(
        string="With product Lines",
        compute="_compute_invoice_with_produt_lines",
        store=True,
    )

    @api.depends("move_type", "line_ids", "line_ids.display_type")
    def _compute_invoice_with_produt_lines(self):
        invoice_types = {"out_invoice", "out_refund", "in_invoice", "in_refund"}
        for move in self:
            if move.move_type not in invoice_types:
                move.invoice_with_produt_lines = False
                continue
            move.invoice_with_produt_lines = not any(
                line.display_type == "product" for line in move.line_ids
            )
