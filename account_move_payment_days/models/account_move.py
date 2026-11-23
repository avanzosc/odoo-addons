# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    days_until_payment_available = fields.Boolean(
        string="Payment Days Available",
        compute="_compute_days_until_payment",
        store=True,
        help=(
            "Indicates whether the invoice has valid dates "
            "for calculating payment days."
        ),
    )

    days_until_payment = fields.Float(
        compute="_compute_days_until_payment",
        store=True,
        aggregator="avg",
        digits=(16, 2),
        help=(
            "Number of days between the accounting date and the "
            "payment or due date, depending on the payment mode. "
            "Negative values are considered zero."
        ),
    )

    @api.depends(
        "move_type",
        "state",
        "date",
        "invoice_date_due",
        "full_reconcile_payment_date",
        "payment_mode_id",
        "payment_mode_id.payment_days_basis",
    )
    def _compute_days_until_payment(self):
        for move in self:
            move.days_until_payment = 0.0
            move.days_until_payment_available = False

            if (
                move.move_type != "in_invoice"
                or move.state != "posted"
                or not move.date
                or not move.payment_mode_id
            ):
                continue

            if move.payment_mode_id.payment_days_basis == "payment":
                end_date = move.full_reconcile_payment_date
            else:
                end_date = move.invoice_date_due

            if not end_date:
                continue

            move.days_until_payment = max(
                0,
                (end_date - move.date).days,
            )
            move.days_until_payment_available = True
