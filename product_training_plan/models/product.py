# -*- coding: utf-8 -*-
# Copyright (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_template_training_ids = fields.One2many(
        comodel_name='product.training.plan', copy=True,
        inverse_name='product_tmpl_id', string='Training plans')


class ProductProduct(models.Model):
    _inherit = 'product.product'

    product_training_ids = fields.One2many(
        comodel_name='product.training.plan', inverse_name='product_id',
        string='Training plans', copy=True)
    template_training_ids = fields.Many2many(
        comodel_name='product.training.plan', string='Template training plans',
        compute='_compute_template_training_ids')

    @api.depends('product_tmpl_id',
                 'product_tmpl_id.product_template_training_ids')
    def _compute_template_training_ids(self):
        for record in self:
            record.template_training_ids =\
                record.product_tmpl_id.product_template_training_ids.filtered(
                    lambda p: not p.product_id)


class ProductTrainingPlan(models.Model):
    _name = 'product.training.plan'
    _description = 'Product training plan'
    _rec_name = 'product_id'
    _order = 'product_tmpl_id, product_id, sequence asc'

    product_tmpl_id = fields.Many2one(
        comodel_name='product.template', string='Product template',
        required=True)
    product_id = fields.Many2one(
        comodel_name='product.product', string='Product')
    sequence = fields.Integer(string='Sequence')
    training_plan_id = fields.Many2one(
        comodel_name='training.plan', string='Training Plan',
        required=True)
    training_plan_code = fields.Char(
        string='Code', related='training_plan_id.code')
