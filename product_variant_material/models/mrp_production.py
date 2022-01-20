# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class MrpProductio(models.Model):
    _inherit = "mrp.production"

    material_id = fields.Many2one(
        string='Material', comodel_name='product.material',
        related='product_id.material_id', store=True)
