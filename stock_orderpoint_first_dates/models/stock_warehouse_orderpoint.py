# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockWarehouseOrderpoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"

    first_reception_date = fields.Date(compute="_compute_first_reception_shipping_date")
    first_shipping_date = fields.Date(compute="_compute_first_reception_shipping_date")

    def _compute_first_reception_shipping_date(self):
        for orderpoint in self:
            first_reception_date = False
            first_shipping_date = False
            moves = orderpoint.product_id.stock_move_ids.filtered(
                lambda x: x.location_dest_id == orderpoint.location_id
                and x.location_id.usage != "internal"
                and x.date_deadline_without_hour > fields.Date.context_today(self)
                and x.state not in ("draft", "cancel", "done")
            )
            if moves:
                first_reception_date = min(moves.mapped("date_deadline_without_hour"))
            moves = orderpoint.product_id.stock_move_ids.filtered(
                lambda x: x.location_id == orderpoint.location_id
                and x.location_dest_id.usage != "internal"
                and x.date_deadline_without_hour > fields.Date.context_today(self)
                and x.state not in ("draft", "cancel", "done")
            )
            if moves:
                first_shipping_date = min(moves.mapped("date_deadline_without_hour"))
            orderpoint.first_reception_date = first_reception_date
            orderpoint.first_shipping_date = first_shipping_date
