# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    standard_shipping = fields.Float(
        compute="_compute_shipping_cost",
    )
    tax_shipping = fields.Float(
        compute="_compute_shipping_cost",
    )
    total_shipping = fields.Float(
        compute="_compute_shipping_cost",
    )
    product = fields.Float(
        compute="_compute_shipping_cost",
    )
    product_tax = fields.Float(
        compute="_compute_shipping_cost",
    )
    product_total = fields.Float(
        compute="_compute_shipping_cost",
    )

    @api.depends(
        "invoice_line_ids",
        "invoice_line_ids.price_subtotal",
        "invoice_line_ids.price_unit",
    )
    def _compute_shipping_cost(self):
        for move in self:
            shipping_products = (
                self.env["delivery.carrier"].search([]).mapped("product_id")
            )
            standard_shipping = total_shipping = product = product_total = 0
            for line in move.invoice_line_ids:
                if line.product_id in shipping_products:
                    standard_shipping += line.price_subtotal
                    total_shipping += line.price_unit
                else:
                    product += line.price_subtotal
                    product_total += line.price_unit
            move.standard_shipping = standard_shipping
            move.total_shipping = total_shipping
            move.tax_shipping = total_shipping - standard_shipping
            move.product = product
            move.product_total = product_total
            move.product_tax = product_total - product
