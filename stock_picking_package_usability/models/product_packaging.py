# Copyright 2021 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductPackaging(models.Model):
    _inherit = "product.packaging"

    empty_weight = fields.Float(
        string="weight empty",
    )
