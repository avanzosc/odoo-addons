# -*- coding: utf-8 -*-
# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    lot_status_id = fields.Many2one(
        comodel_name='stock.production.lot.status', string='Lot status',
        related='lot_id.lot_status_id', store=True)
