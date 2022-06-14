# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    price_total_eur = fields.Monetary(
        string="Total EUR", compute="_compute_price_total_eur", store=True,
        copy=False)
    price_subtotal_eur = fields.Monetary(
        string="SubTotal EUR", compute="_compute_price_total_eur", store=True,
        copy=False)

    @api.depends("order_line", "order_line.price_total_eur",
                 "order_line.price_subtotal_eur")
    def _compute_price_total_eur(self):
        for purchase in self:
            purchase.price_total_eur = sum(
                purchase.order_line.mapped("price_total_eur"))
            purchase.price_subtotal_eur = sum(
                purchase.order_line.mapped("price_subtotal_eur"))
