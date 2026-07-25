# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    pricing_method = fields.Selection(
        selection=[
            ("qty", "Quantity"),
            ("weight", "Weight"),
            ("length", "Length"),
            ("wl", "Weight*Length"),
        ],
    )
