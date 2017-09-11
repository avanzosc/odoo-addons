# -*- coding: utf-8 -*-
# Copyright 2015-2017 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class ProductCategory(models.Model):
    _inherit = 'product.category'

    sequence_id = fields.Many2one(
        comodel_name='ir.sequence', string='Sequence')


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def create(self, values):
        if not values.get('default_code'):
            categ = self.env['product.category'].browse(values.get('categ_id'))
            values['default_code'] = (
                categ.sequence_id.next_by_id(categ.sequence_id.id))
        return super(ProductProduct, self).create(values)

    @api.multi
    def write(self, values):
        for record in self:
            if 'categ_id' in values and not values.get('default_code',
                                                       record.default_code):
                categ = self.env['product.category'].browse(
                    values.get('categ_id'))
                values['default_code'] = categ.sequence_id.next_by_id(
                    categ.sequence_id.id)
            super(ProductProduct, record).write(values)
        return True

    @api.multi
    def rewrite_default_code(self):
        for record in self.filtered('categ_id.sequence_id'):
            record.write({
                'categ_id': record.categ_id.id,
                'default_code': False
            })
        return True


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def create(self, values):
        if not values.get('default_code', False):
            categ = self.env['product.category'].browse(values.get('categ_id'))
            values['default_code'] = (
                categ.sequence_id.next_by_id(categ.sequence_id.id))
        return super(ProductTemplate, self).create(values)

    @api.multi
    def write(self, values):
        for record in self:
            if 'categ_id' in values and not values.get('default_code',
                                                       record.default_code):
                categ = self.env['product.category'].browse(
                    values.get('categ_id'))
                values['default_code'] = categ.sequence_id.next_by_id(
                    categ.sequence_id.id)
            super(ProductTemplate, record).write(values)
        return True

    @api.multi
    def rewrite_default_code(self):
        for record in self.filtered('categ_id.sequence_id'):
            record.write({
                'categ_id': record.categ_id.id,
                'default_code': False
            })
        return True
