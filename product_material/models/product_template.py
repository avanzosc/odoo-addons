# Copyright 2021 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    material_id = fields.Many2one(
        string='Material', comodel_name='product.material')
