# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from datetime import timedelta

from odoo import fields, models
from odoo.tools.float_utils import float_round


class ProductProduct(models.Model):
    _inherit = "product.product"

    move_line_ids = fields.One2many(
        string="Product Move Lines",
        comodel_name="stock.move.line",
        inverse_name="product_id",
        copy=False,
    )
    consumed_last_twelve_months = fields.Float(
        string="Consumed last twelve months",
        digits="Product Unit of Measure",
        compute="_compute_consumed_last_twelve_months",
    )
    months_with_stock = fields.Integer(
        string="Months with stock", compute="_compute_months_with_stock"
    )

    def _compute_consumed_last_twelve_months(self):
        date_from = fields.Datetime.to_string(
            fields.datetime.now() - timedelta(days=365)
        )
        date_from = fields.Datetime.from_string(date_from)
        for product in self:
            consumed_last_twelve_months = 0
            lines = product.move_line_ids.filtered(
                lambda x: x.state == "done"
                and x.date > date_from
                and x.location_dest_id is not False
                and x.location_dest_id.usage not in ("view", "internal", "supplier")
            )
            if lines:
                consumed_last_twelve_months = float_round(
                    sum(lines.mapped("qty_done")),
                    precision_rounding=product.uom_id.rounding,
                )
            product.consumed_last_twelve_months = consumed_last_twelve_months

    def _compute_months_with_stock(self):
        for product in self:
            months_with_stock = 0
            consumed_last_twelve_months = product.consumed_last_twelve_months
            if consumed_last_twelve_months:
                months_with_stock = product.virtual_available / (
                    consumed_last_twelve_months / 12
                )
            product.months_with_stock = months_with_stock
