# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    sequence_id = fields.Many2one(
        string="Sequence", comodel_name="ir.sequence", copy=False
    )
