# Copyright 2023 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    paid_date = fields.Date(
        compute="_compute_paid_date",
        store=True,
        copy=False,
        readonly=True,
    )
    payment_period = fields.Integer(
        compute="_compute_payment_period",
        store=True,
        copy=False,
        readonly=True,
    )

    @api.depends("payment_state")
    def _compute_paid_date(self):
        for move in self:
            move.paid_date = (
                fields.Date.context_today(move)
                if move.payment_state == "paid"
                else False
            )

    @api.depends("paid_date", "invoice_date")
    def _compute_payment_period(self):
        for move in self:
            period = 0
            if move.paid_date and move.invoice_date:
                period = (move.paid_date - move.invoice_date).days
            move.payment_period = period
