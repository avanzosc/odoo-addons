# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models


class ProcurementSaleForecastLine(models.Model):
    _inherit = 'procurement.sale.forecast.line'

    def _find_sale_forecast(
            self, from_date, to_date, product, location):
        cond = [('product_id', '=', product.id),
                ('date', '>=', from_date),
                ('date', '<=', to_date),
                ('procurement_id', '=', False)]
        forecast_lines = self.search(cond)
        forecast_lines = forecast_lines.filtered(
            lambda x: x.forecast_id.warehouse_id.lot_stock_id.id ==
            location.id)
        return forecast_lines
