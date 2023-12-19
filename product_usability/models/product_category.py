# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductCategory(models.Model):
    _inherit = 'product.category'

    root_category_id = fields.Many2one(
        comodel_name='product.category', string='Root Category',
        compute='_compute_root_category', store=True)

    @api.multi
    @api.depends('parent_id', 'parent_id.root_category_id')
    def _compute_root_category(self):
        for categ in self:
            if categ.parent_id:
                categ.root_category_id = categ.parent_id.root_category_id
            else:
                categ.root_category_id = categ
