# -*- coding: utf-8 -*-
# © 2017 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models


class ProductAttributeValue(models.Model):
    _inherit = 'product.attribute.value'

    operation_ids = fields.Many2many(comodel_name='mrp.routing.operation',
                                     String='Operations')
