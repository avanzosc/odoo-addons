# -*- coding: utf-8 -*-
# Copyright © 2019 Oihana Larrañaga - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models, api


class ProductProduct(models.Model):
    _inherit = "product.product"

    reserved = fields.Float(
        string='Reserved', compute='_compute_reserved', store=True)
    quants_ids = fields.One2many(comodel_name='stock.quant',
                                 inverse_name='product_id')

    @api.depends('quants_ids', 'quants_ids.qty')
    def _compute_reserved(self):
        for product in self:
            quants = product.mapped('quants_ids').filtered(
                lambda c: c.location_id and
                c.location_id.usage == 'internal' and c.reservation_id)
            product.reserved = sum(quants.mapped('qty'))
