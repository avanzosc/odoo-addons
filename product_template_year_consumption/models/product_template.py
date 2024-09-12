# © 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3 - See https://www.gnu.org/licenses/agpl-3.0.html

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    year_consumption = fields.Float(string="Consumption in a Year", default=0)
    month_forecast = fields.Float(
        string="Month Forecast", compute="_compute_month_forecast"
    )

    consumed_last_twelve_months = fields.Float(
        string="Consumed last twelve months",
        digits="Product Unit of Measure",
        compute="_compute_consumed_last_twelve_months",
    )
    months_with_stock = fields.Integer(
        string="Months with stock", compute="_compute_months_with_stock"
    )

    def action_update_product_consumption(self):
        self.ensure_one()
        today = fields.Datetime.now()
        last_year = today + relativedelta(years=-1)
        cond = [
            ("product_id", "=", self.product_variant_id.id),
            ("date", ">", last_year),
            ("date", "<=", today),
        ]
        moves = self.env["stock.move"].search(cond)
        qty_sum = 0
        for line in moves.filtered(
            lambda c: c.location_dest_id.usage not in ("internal", "view")
        ):
            qty_sum += line.product_uom_qty
        self.year_consumption = qty_sum

    @api.depends("year_consumption", "qty_available", "outgoing_qty")
    def _compute_month_forecast(self):
        for product in self:
            product.month_forecast = 0
            if product.year_consumption != 0:
                product.month_forecast = (
                    product.qty_available - product.outgoing_qty
                ) / (product.year_consumption / 12)

    def _compute_consumed_last_twelve_months(self):
        for template in self:
            consumed_last_twelve_months = 0
            if len(template.product_variant_ids) == 1:
                consumed_last_twelve_months = template.product_variant_ids[
                    0
                ].consumed_last_twelve_months
            template.consumed_last_twelve_months = consumed_last_twelve_months

    def _compute_months_with_stock(self):
        for template in self:
            months_with_stock = 0
            if len(template.product_variant_ids) == 1:
                months_with_stock = template.product_variant_ids[0].months_with_stock
            template.months_with_stock = months_with_stock
