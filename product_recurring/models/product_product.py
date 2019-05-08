# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class ProductProduct(models.Model):
    _inherit = 'product.product'

    recurrent_punctual = fields.Selection(
        selection=[('recurrent', 'Recurrent'),
                   ('punctual', 'Punctual')], string='Recurrent/Punctual')
    punctual_month_ids = fields.Many2many(
        comodel_name='base.month', string='Punctual months',
        relation='rel_product_base_month',
        column1='product_id', column2='month_id')
