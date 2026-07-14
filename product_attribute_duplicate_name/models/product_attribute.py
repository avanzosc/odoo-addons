# Copyright 2026 Ane Gurruchaga - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    _sql_constraints = [
        ("number_uniq", "CHECK(name IS NOT NULL)", "Attribute name is required!"),
    ]
