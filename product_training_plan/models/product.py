# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_template_training_ids = fields.One2many(
        comodel_name='product.training.plan', copy=True,
        inverse_name='product_tmpl_id', string='Training plan')


class ProductProduct(models.Model):
    _inherit = 'product.product'

    product_training_ids = fields.One2many(
        comodel_name='product.training.plan', inverse_name='product_id',
        string='Training plan', copy=True)


class ProductTrainingPlan(models.Model):
    _name = 'product.training.plan'
    _description = 'Product training plan'
    _rec_name = 'product_id'
    _order = 'product_tmpl_id, product_id, sequence asc'

    product_tmpl_id = fields.Many2one(
        comodel_name='product.template', string='Product template')
    product_id = fields.Many2one(
        comodel_name='product.product', string='Product')
    sequence = fields.Integer(string="Sequence")
    training_plan_id = fields.Many2one(
        comodel_name='training.plan', string='Training Plan')

    _sql_constraints = [
        ('product_training_plan_unique', 'unique(product_tmpl_id, product_id,'
         ' sequence)',
         _('You can not create two training plans with same sequence for one'
           ' product template/product.'))]
