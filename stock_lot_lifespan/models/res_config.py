# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api


class StockConfigSettings(models.TransientModel):

    _inherit = 'stock.config.settings'

    stock_lot_percentage1 = fields.Float(
        string='Lot Lifespan Percentage 1.')
    stock_lot_percentage2 = fields.Float(
        string='Lot Lifespan Percentage 2.')
    stock_lot_percentage3 = fields.Float(
        string='Lot Lifespan Percentage 3.')

    @api.multi
    def get_default_stock_lot_percentage(self, fields):
        stock_lot_percentage_1 = self.env.ref(
            'stock_lot_lifespan.config_stock_lot_percentage_1').value
        stock_lot_percentage_2 = self.env.ref(
            'stock_lot_lifespan.config_stock_lot_percentage_2').value
        stock_lot_percentage_3 = self.env.ref(
            'stock_lot_lifespan.config_stock_lot_percentage_3').value
        return {
            'stock_lot_percentage1': float(stock_lot_percentage_1),
            'stock_lot_percentage2': float(stock_lot_percentage_2),
            'stock_lot_percentage3': float(stock_lot_percentage_3),
            }

    @api.multi
    def set_default_stock_lot_percentage(self):
        self.env['ir.config_parameter'].set_param(
            'stock_lot_percentage1', self.stock_lot_percentage1 or '0.0')
        self.env['ir.config_parameter'].set_param(
            'stock_lot_percentage2', self.stock_lot_percentage2 or '0.0')
        self.env['ir.config_parameter'].set_param(
            'stock_lot_percentage3', self.stock_lot_percentage3 or '0.0')
