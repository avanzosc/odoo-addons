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
