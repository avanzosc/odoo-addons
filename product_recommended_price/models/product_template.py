# Copyright Bernabé Olavarrieta - Alquemy
# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    recommended_price = fields.Float(
        string="Recommended price",
        digits="Product Price",
    )
