# -*- coding: utf-8 -*-
# Copyright 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields


class ProductCategory(models.Model):
    _inherit = 'product.category'

    default_location = fields.Many2one(
        comodel_name='stock.location', string='Default location')


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    default_location = fields.Many2one(
        comodel_name='stock.location', string='Default location')
