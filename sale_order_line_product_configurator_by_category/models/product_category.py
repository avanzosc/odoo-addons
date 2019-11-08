# Copyright 2019 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    restricted_by = fields.Many2one(comodel_name="product.category",
                                    string="Restricted For")
