# -*- coding: utf-8 -*-
# Copyright 2018 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, api


class StockQuant(models.Model):

    _inherit = 'stock.quant'
    _order = 'in_date asc'

    @api.model
    def _quant_split(self, quant, qty):
        new_quant = super(StockQuant, self)._quant_split(quant, qty)
        relation_move = self.env.context.get('load_move_relation', False)
        if relation_move:
            relation_move.quant_ids = [(4, quant.id)]
            if new_quant:
                relation_move.quant_ids = [(4, new_quant.id)]
        return new_quant
