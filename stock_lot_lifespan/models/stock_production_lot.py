# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api
from dateutil.relativedelta import relativedelta


class StockProductionLot(models.Model):

    _inherit = 'stock.production.lot'

    @api.onchange('mrp_date', 'life_date')
    @api.multi
    def onchange_mrp_life_date(self):
        self.ensure_one()
        if not self.mrp_date or not self.life_date:
            return {}
        stock_config_model = self.env['stock.config.settings']
        mrp_date = fields.Date.from_string(self.mrp_date)
        life_date = fields.Date.from_string(self.life_date)
        lifespan = (life_date - mrp_date).days
        vals = stock_config_model.get_default_stock_lot_percentage([])
        variation1 = lifespan * vals.get('stock_lot_percentage1', 0) / 100
        variation2 = lifespan * vals.get('stock_lot_percentage2', 0) / 100
        variation3 = lifespan * vals.get('stock_lot_percentage3', 0) / 100
        self.alert_date = mrp_date + relativedelta(days=variation1)
        self.removal_date = mrp_date + relativedelta(days=variation2)
        self.use_date = mrp_date + relativedelta(days=variation3)
