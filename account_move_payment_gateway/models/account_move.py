# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    shopify_payment_gateway_ids = fields.Many2many(
        comodel_name="shopify.payment.gateway.ept",
        compute="_compute_shopify_payment_gateway_ids",
    )

    @api.depends(
        "invoice_line_ids.sale_line_ids.order_id.shopify_payment_gateway_id",
    )
    def _compute_shopify_payment_gateway_ids(self):
        for move in self:
            gateways = move.invoice_line_ids.mapped(
                "sale_line_ids.order_id.shopify_payment_gateway_id"
            )
            move.shopify_payment_gateway_ids = gateways.filtered(lambda g: g)
