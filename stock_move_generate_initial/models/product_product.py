# -*- coding: utf-8 -*-
# Copyright 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.depends('move_ids')
    def _compute_with_moves(self):
        for product in self:
            product.with_moves = bool(product.move_ids)

    move_ids = fields.One2many(
        comodel_name='stock.move', inverse_name='product_id',
        string='Stock moves')
    with_moves = fields.Boolean(
        string='With moves', compute='_compute_with_moves', store=True)
