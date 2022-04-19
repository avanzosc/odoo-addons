# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class ProductTemlate(models.Model):
    _inherit = 'product.template'

    template_category_type_id = fields.Many2one(
        string='Category type', comodel_name='category.type', store=True,
        related='categ_id.type_id')
