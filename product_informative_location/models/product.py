# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api


class ProductInformativeLocationPrecision1(models.Model):
    _name = 'product.informative.location.precision1'
    _description = 'Product informative location precision 1'
    _order = 'name'

    name = fields.Char(string='Code')
    description = fields.Char(string='Description')


class ProductInformativeLocationPrecision2(models.Model):
    _name = 'product.informative.location.precision2'
    _description = 'Product informative location precision 2'
    _order = 'name'

    name = fields.Char(string='Code')
    description = fields.Char(string='Description')


class ProductInformativeLocationPrecision3(models.Model):
    _name = 'product.informative.location.precision3'
    _description = 'Product informative location precision 3'
    _order = 'name'

    name = fields.Char(string='Code')
    description = fields.Char(string='Description')


class ProductInformativeLocation(models.Model):
    _name = 'product.informative.location'
    _description = 'Product informative location'
    _order = 'product_id, location_id, sequence'

    name = fields.Char(
        string='Code', compute='_compute_name', store=True)
    description = fields.Char(
        string='Description', compute='_compute_name', store=True)
    product_id = fields.Many2one(
        string='Product', comodel_name='product.product')
    location_id = fields.Many2one(
        string='Location', comodel_name='stock.location')
    sequence = fields.Integer(
        string='Sequence', default=1)
    precision1_id = fields.Many2one(
        string='Precision 1',
        comodel_name='product.informative.location.precision1')
    precision1_description = fields.Char(
        string='Precision 1 description', related='precision1_id.description',
        store=True)
    precision2_id = fields.Many2one(
        string='Precision 2',
        comodel_name='product.informative.location.precision2')
    precision2_description = fields.Char(
        string='Precision 2 description', related='precision2_id.description',
        store=True)
    precision3_id = fields.Many2one(
        string='Precision 3',
        comodel_name='product.informative.location.precision3')
    precision3_description = fields.Char(
        string='Precision 3 description', related='precision3_id.description',
        store=True)

    @api.depends('precision1_id', 'precision2_id', 'precision3_id',
                 'precision1_id.name', 'precision2_id.name',
                 'precision3_id.name', 'precision1_id.description',
                 'precision2_id.description', 'precision3_id.description')
    def _compute_name(self):
        for record in self:
            name = record.precision1_id.name
            desc = record.precision1_id.description
            if record.precision2_id:
                name = '{} - {}'.format(name, record.precision2_id.name)
                desc = '{} - {}'.format(desc, record.precision2_id.description)
            if record.precision3_id:
                name = '{} - {}'.format(name, record.precision3_id.name)
                desc = '{} - {}'.format(desc, record.precision3_id.description)
            record.name = name
            record.description = desc


class ProductProduct(models.Model):
    _inherit = 'product.product'

    product_location_ids = fields.One2many(
        string='Product informative locations', inverse_name='product_id',
        comodel_name='product.informative.location')
