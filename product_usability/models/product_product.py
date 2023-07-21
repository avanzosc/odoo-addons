# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from datetime import timedelta

from odoo import fields, models
from odoo.tools.float_utils import float_round


class ProductProduct(models.Model):
    _inherit = "product.product"

    comsumed_last_twelve_months = fields.Float(
        string="Consumed last twelve months",
        digits="Product Unit of Measure",
        compute="_compute_comsumed_last_twelve_months",
    )
    months_with_stock = fields.Integer(
        string="Months with stock", compute="_compute_months_with_stock"
    )

    def _compute_comsumed_last_twelve_months(self):
        stock_move_obj = self.env["stock.move"]
        date_from = fields.Datetime.to_string(
            fields.datetime.now() - timedelta(days=365)
        )
        for product in self:
            domain = [
                ("state", "=", "done"),
                ("date", ">", date_from),
                ("location_dest_id", "!=", False),
                ("location_dest_id.usage", "not in", ("view", "internal", "supplier")),
                ("product_id", "=", product.id),
            ]
            move_lines = stock_move_obj.read_group(
                domain, ["product_id", "product_uom_qty"], ["product_id"]
            )
            move_data = {
                data["product_id"][0]: data["product_uom_qty"] for data in move_lines
            }
            product.comsumed_last_twelve_months = float_round(
                move_data.get(product.id, 0), precision_rounding=product.uom_id.rounding
            )

    def _compute_months_with_stock(self):
        for product in self:
            months_with_stock = 0
            if product.incoming_qty:
                months_with_stock = (
                    product.qty_available + product.incoming_qty - product.outgoing_qty
                ) / (product.incoming_qty / 12)
            product.months_with_stock = months_with_stock
