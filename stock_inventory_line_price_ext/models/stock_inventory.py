# -*- coding: utf-8 -*-
# Copyright 2019 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import api, fields, models
import openerp.addons.decimal_precision as dp


class StockInventoryLine(models.Model):
    _inherit = "stock.inventory.line"

    theoretical_subtotal = fields.Float('Theoretical subtotal',
                                        compute="_compute_subtotals",
                                        digits=dp.get_precision(
                                            'Product Price'))
    real_subtotal = fields.Float('Real subtotal', compute="_compute_subtotals",
                                 digits=dp.get_precision('Product Price'))

    @api.depends('theoretical_std_price', 'standard_price', 'product_qty')
    def _compute_subtotals(self):
        for inventory in self:
            qty = inventory.product_qty
            inventory.theoretical_subtotal = inventory.theoretical_std_price *\
                qty
            inventory.real_subtotal = inventory.standard_price * qty
