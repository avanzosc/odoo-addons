# -*- coding: utf-8 -*-
# Copyright 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models
import openerp.addons.decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    price1 = fields.Float(
        string='First price', digits=dp.get_precision('Product Price'))
    price2 = fields.Float(
        string='Second price', digits=dp.get_precision('Product Price'))
    price3 = fields.Float(
        string='Third price', digits=dp.get_precision('Product Price'))
    price4 = fields.Float(
        string='Fourth price', digits=dp.get_precision('Product Price'))


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _compute_number_price_field(self):
        a = self.env['base.config.settings'].get_default_number_price_field()
        self.number_price_field = a.get('number_price_field')

    price1 = fields.Float(
        string='First price', digits=dp.get_precision('Product Price'))
    price2 = fields.Float(
        string='Second price', digits=dp.get_precision('Product Price'))
    price3 = fields.Float(
        string='Third price', digits=dp.get_precision('Product Price'))
    price4 = fields.Float(
        string='Fourth price', digits=dp.get_precision('Product Price'))
    number_price_field = fields.Selection(
        selection=[('2', '2'), ('3', '3'), ('4', '4')],
        string='Prices in products',
        compute='_compute_number_price_field')
