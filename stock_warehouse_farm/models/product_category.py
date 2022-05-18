# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class ProductCategory(models.Model):
    _inherit = 'product.category'

    type_id = fields.Many2one(string='Type', comodel_name='category.type')
