# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    price_total_eur = fields.Monetary(
        string="Total EUR", compute="_compute_prices_eur", store=True,
        copy=False)
    price_subtotal_eur = fields.Monetary(
        string="SubTotal EUR", compute="_compute_prices_eur", store=True,
        copy=False)
    origin_price_total = fields.Monetary(
        string="Origin total", compute='_compute_amount', store=True,
        copy=False)
    origin_price_subtotal = fields.Monetary(
        string="Origin Subtotal", compute='_compute_amount', store=True,
        copy=False)

    @api.depends("origin_price_total", "origin_price_subtotal", "state")
    def _compute_prices_eur(self):
        for line in self:
            if line.currency_id == line.company_id.currency_id:
                line.price_total_eur = line.price_total
                line.price_subtotal_eur = line.price_subtotal
            else:
                line.price_total_eur = (
                    line.price_total / line.currency_id.rate)
                line.price_subtotal_eur = (
                    line.price_subtotal / line.currency_id.rate)

    @api.depends("product_qty", "price_unit", "taxes_id")
    def _compute_amount(self):
        result = super(PurchaseOrderLine, self)._compute_amount()
        for line in self:
            line.origin_price_total = line.price_total
            line.origin_price_subtotal = line.price_subtotal
        return result
