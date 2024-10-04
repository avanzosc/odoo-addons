# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import pytz

from odoo import fields, models


class StockWarehouseOrderpoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"

    first_reception_date = fields.Date(compute="_compute_first_reception_date_purchase")
    first_reception_purchase_id = fields.Many2one(
        string="First Reception Purchase",
        comodel_name="purchase.order",
        compute="_compute_first_reception_date_purchase",
    )
    first_shipping_date = fields.Date(compute="_compute_first_shipping_date_sale")

    first_shipping_sale_id = fields.Many2one(
        string="First Shipping Sale",
        comodel_name="sale.order",
        compute="_compute_first_shipping_date_sale",
    )

    def _compute_first_reception_date_purchase(self):
        for orderpoint in self:
            first_reception_date = False
            first_reception_purchase_id = False
            moves = orderpoint.product_id.move_ids.filtered(
                lambda x: x.location_dest_id == orderpoint.location_id
                and x.state not in ("cancel", "done")
                and x.purchase_line_id
            )
            if moves:
                purchase_lines = moves.mapped("purchase_line_id")
                purchases = purchase_lines.mapped("order_id")
                purchases = purchases.filtered(
                    lambda z: z.date_planned_without_hour
                    >= fields.Date.context_today(self)
                )
                if purchases:
                    first_purchase = min(
                        purchases, key=lambda x: x.date_planned_without_hour
                    )
                    first_reception_purchase_id = first_purchase.id
                    first_reception_date = first_purchase.date_planned_without_hour
            orderpoint.first_reception_date = first_reception_date
            orderpoint.first_reception_purchase_id = first_reception_purchase_id

    def _compute_first_shipping_date_sale(self):
        for orderpoint in self:
            first_shipping_date = False
            first_shipping_sale_id = False
            moves = orderpoint.product_id.move_ids.filtered(
                lambda x: x.location_id == orderpoint.location_id
                and x.state not in ("cancel", "done")
                and x.sale_line_id
            )
            for move in moves:
                expected_date = False
                if move.sale_line_id.order_id.expected_date:
                    local_dt = move.sale_line_id.order_id.expected_date.astimezone(
                        pytz.timezone(self.env.user.tz or "UTC")
                    )
                    expected_date = local_dt.date()
                if expected_date and expected_date >= fields.Date.context_today(self):
                    if not first_shipping_date or expected_date < first_shipping_date:
                        first_shipping_date = expected_date
                        first_shipping_sale_id = move.sale_line_id.order_id.id
            orderpoint.first_shipping_date = first_shipping_date
            orderpoint.first_shipping_sale_id = first_shipping_sale_id
