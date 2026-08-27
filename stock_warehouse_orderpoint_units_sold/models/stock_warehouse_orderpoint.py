# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class StockWarehouseOrderpoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"

    sold = fields.Float(digits="Product Unit of Measure", default=0)
    billed = fields.Float(digits="Product Unit of Measure", default=0)
    forecast_sold = fields.Float(digits="Product Unit of Measure", default=0)
    billed_forecast = fields.Float(digits="Product Unit of Measure", default=0)

    @api.onchange("supplier_id")
    def onchange_supplier_id(self):
        self.update_forecast_info()

    def ir_cron_update_forecast_info(self):
        orderpoints = self.env["stock.warehouse.orderpoint"].search([])
        orderpoints.update_forecast_info()

    def update_forecast_info(self):
        today = fields.Date.today()
        last_year = today + relativedelta(years=-1)
        for orderpoint in self:
            cond = [
                ("product_id", "=", orderpoint.product_id.id),
                ("state", "=", "done"),
                ("order_id.date_order", ">=", last_year),
            ]
            lines = self.env["sale.order.line"].search(cond)
            sold = sum(lines.mapped("product_uom_qty")) if lines else 0
            billed = sum(lines.mapped("qty_invoiced")) if lines else 0
            if orderpoint.supplier_id:
                monthly_forecast = orderpoint.supplier_id.partner_id.monthly_forecast
            else:
                seller = orderpoint.product_id._select_seller(
                    partner_id=False,
                    quantity=0.0,
                    date=today,
                    uom_id=orderpoint.product_id.uom_po_id,
                    params=False,
                )
                monthly_forecast = seller.partner_id.monthly_forecast if seller else 0
            forecast_sold = sold / monthly_forecast if monthly_forecast else 0
            billed_forecast = billed / monthly_forecast if monthly_forecast else 0
            orderpoint.write(
                {
                    "sold": sold,
                    "billed": billed,
                    "forecast_sold": forecast_sold,
                    "billed_forecast": billed_forecast,
                }
            )
