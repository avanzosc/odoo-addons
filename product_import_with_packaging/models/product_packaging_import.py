# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductPackagingImport(models.Model):
    _inherit = "product.packaging.import"

    data = fields.Binary(
        required=False,
    )
