# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    category_type_id = fields.Many2one(
        string='Type',
        comodel_name='category.type',
        related='categ_id.type_id',
        store=True)
