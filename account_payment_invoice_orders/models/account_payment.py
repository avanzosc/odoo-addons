# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class AccountPayment(models.Model):
    _inherit = "account.payment"

    sale_order_ids = fields.Many2many(
        string="Sale Orders",
        comodel_name="sale.order",
        relation="rel_sale_payment",
        column1="payment_id",
        column2="sale_id",
    )
    sale_amount = fields.Float(
        string="Sale Amount", compute="_compute_sale_amount", store=True
    )
    invoice_order_ids = fields.Many2many(
        string="Invoice Orders",
        comodel_name="account.move",
        relation="rel_invoice_payment",
        column1="payment_id",
        column2="invoice_id",
    )
    invoice_amount = fields.Float(
        string="Invoice Amount", compute="_compute_invoice_amount", store=True
    )
    purchase_order_ids = fields.Many2many(
        string="Purchase",
        comodel_name="purchase.order",
        relation="rel_purchase_payment",
        column1="payment_id",
        column2="purchase_id",
    )
    purchase_amount = fields.Float(
        string="Purchase Amount", compute="_compute_purchase_amount", store=True
    )

    @api.depends("partner_id", "sale_order_ids")
    def _compute_sale_amount(self):
        for payment in self:
            amount = 0
            if payment.sale_order_ids:
                amount = sum(payment.sale_order_ids.mapped("amount_total"))
            payment.sale_amount = amount

    @api.depends("partner_id", "invoice_order_ids")
    def _compute_invoice_amount(self):
        for payment in self:
            amount = 0
            if payment.invoice_order_ids:
                amount = sum(payment.invoice_order_ids.mapped("amount_total_signed"))
            payment.invoice_amount = amount

    @api.depends("partner_id", "purchase_order_ids")
    def _compute_purchase_amount(self):
        for payment in self:
            amount = 0
            if payment.purchase_order_ids:
                amount = sum(payment.purchase_order_ids.mapped("amount_total"))
            payment.purchase_amount = amount

    @api.onchange("partner_id")
    def onchange_partner_id(self):
        if self.partner_id:
            sales = []
            purchases = []
            invoices = []
            for line in self.env["sale.order"].search(
                [("state", "=", "sale"), ("partner_id", "=", self.partner_id.id)]
            ):
                if not line.invoice_ids or line.invoice_ids.filtered(
                    lambda c: c.state == "posted"
                    and c.payment_state in ("not_paid", "partial")
                ):
                    sales.append(line.id)
            for line in self.env["purchase.order"].search(
                [("state", "=", "purchase"), ("partner_id", "=", self.partner_id.id)]
            ):
                if not line.invoice_ids or line.invoice_ids.filtered(
                    lambda c: c.state == "posted"
                    and c.payment_state in ("not_paid", "partial")
                ):
                    purchases.append(line.id)
            for line in self.env["account.move"].search(
                [
                    ("payment_state", "in", ("not_paid", "in_payment", "partial")),
                    ("partner_id", "=", self.partner_id.id),
                    ("move_type", "in", ("out_refund", "out_invoice")),
                ]
            ):
                invoices.append(line.id)
            self.sale_order_ids = [(6, 0, sales)]
            self.purchase_order_ids = [(6, 0, purchases)]
            self.invoice_order_ids = [(6, 0, invoices)]

    @api.onchange("invoice_order_ids")
    def onchange_order_ids(self):
        self.amount = self.invoice_amount
