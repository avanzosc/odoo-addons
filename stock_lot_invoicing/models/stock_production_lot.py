# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class StockProductionLot(models.Model):

    _inherit = 'stock.production.lot'

    cost_price = fields.Float(string="Cost Price",
                              digits=dp.get_precision('Product Price'))
    unit_price = fields.Float(string="Unit Price",
                              digits=dp.get_precision('Product Price'))
    percentage = fields.Integer(string="Percentage (%)")

    @api.multi
    @api.onchange('unit_price', 'percentage')
    def onchange_unit_price_percentage(self):
        self.ensure_one()
        self.cost_price = self.unit_price * (float(self.percentage)/100)

    @api.multi
    def write(self, values):
        if 'unit_price' in values or 'percentage' in values:
            self.onchange_unit_price_percentage()
        return super(StockProductionLot, self).write(values)
