# -*- coding: utf-8 -*-
# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    @api.model
    def quants_unreserve(self, move):
        related_moves = self.env['stock.move'].search([
            ('split_from', '=', move.id)])
        related_quants = move.reserved_quant_ids
        super(StockQuant, self).quants_unreserve(move)
        related_quants.sudo().write({
            'reservation_id': related_moves[:1].id})
