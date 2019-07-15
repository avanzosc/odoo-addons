# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api


class StockLocation(models.Model):

    _inherit = 'stock.location'

    stock_on_hand = fields.Boolean(string='Stock On Hand')

    @api.onchange('usage')
    def onchange_usage(self):
        self.ensure_one()
        self.stock_on_hand = bool(self.usage == 'internal')
