# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    discount2_pc = fields.Float(string='Discount Percentage', default=20)
    discount2_product_id = fields.Many2one(
        comodel_name='product.product', string='Discount Product')
    discount3_pc = fields.Float(string='Discount Percentage', default=25)
    discount3_product_id = fields.Many2one(
        comodel_name='product.product', string='Discount Product')
