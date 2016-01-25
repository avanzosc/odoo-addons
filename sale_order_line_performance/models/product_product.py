# -*- coding: utf-8 -*-
# © 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    performance = fields.Float(
        'Performance', help='Estimated time for completion the task')
