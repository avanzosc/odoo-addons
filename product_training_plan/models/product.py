# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    event_track_template2_ids = fields.One2many(
        comodel_name='product.event.track.template', copy=True,
        inverse_name='product_tmpl_id', string='Training plan')


class ProductProduct(models.Model):
    _inherit = 'product.product'

    event_track_template_ids = fields.One2many(
        comodel_name='product.event.track.template', inverse_name='product_id',
        string='Training plan', copy=True)


class ProductEventTrackTemplate(models.Model):
    _name = 'product.event.track.template'
    _description = 'Training plan'
    _rec_name = 'product_id'
    _order = 'product_tmpl_id, product_id, sequence asc'

    product_tmpl_id = fields.Many2one(
        comodel_name='product.template', string='Product template')
    product_id = fields.Many2one(
        comodel_name='product.product', string='Product')
    sequence = fields.Integer(string="Sequence")
    name = fields.Char(string="Description")
    planification = fields.Text(string="Planification")
    resolution = fields.Text(string="Resolution")
    html_info = fields.Html(string='Description', translate=True)
    url = fields.Char(string='URL')

    _sql_constraints = [
        ('track_template_product_unique', 'unique(product_tmpl_id, product_id,'
         ' sequence)',
         _('You can not create two templates with same sequence for one'
           ' product template/product.'))
    ]
