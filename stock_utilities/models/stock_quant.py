# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields
from openerp.addons import decimal_precision as dp


class StockQuant(models.Model):

    _inherit = 'stock.quant'

    qty = fields.Float(digits=dp.get_precision('Product Unit of Measure'))
