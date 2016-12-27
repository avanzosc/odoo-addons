# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields


class ProcurementSaleForecastLine(models.Model):
    _inherit = 'procurement.sale.forecast.line'

    lot_stock_id = fields.Many2one(
        comodel_name='stock.location', string='Location', store=True,
        related='forecast_id.warehouse_id.lot_stock_id')

    def _find_sale_forecast(
            self, from_date, to_date, product, location):
        cond = [('product_id', '=', product.id),
                ('date', '>=', from_date),
                ('date', '<=', to_date),
                ('lot_stock_id', '=', location.id)]
        forecast_lines = self.search(cond)
        return forecast_lines
