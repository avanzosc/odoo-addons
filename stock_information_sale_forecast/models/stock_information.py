# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class StockInformation(models.Model):
    _inherit = 'stock.information'

    @api.multi
    def _compute_week(self):
        forecast_obj = self.env['procurement.sale.forecast.line']
        super(StockInformation, self)._compute_week()
        for line in self:
            sale_forecasts = forecast_obj._find_sale_forecast(
                line.first_day_week, line.last_day_week, line.product,
                line.location)
            line.sale_forecast = sum(sale_forecasts.mapped('qty'))

    sale_forecast = fields.Float(
        'Sale forecast', compute='_compute_week',
        digits=dp.get_precision('Product Unit of Measure'),
        help='Sale forecast')
