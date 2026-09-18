# Copyright 2026 Ana Juaristi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    is_shape = fields.Boolean(string="Shape")
