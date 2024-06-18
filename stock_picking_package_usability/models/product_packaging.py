# Copyright 2021 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductPackaging(models.Model):
    _inherit = "product.packaging"

    packaging_length = fields.Integer(
        string="Pack Length", related="package_type_id.packaging_length", store=True
    )
    width = fields.Integer(
        string="Pack Width", related="package_type_id.width", store=True
    )
    height = fields.Integer(
        string="Pack Height", related="package_type_id.height", store=True
    )
