# Copyright 2026 Ane Gurruchaga - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, models


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    def copy_data(self, default=None):
        default = dict(default or {})
        vals_list = super().copy_data(default=default)
        if "name" not in default:
            for attribute, vals in zip(self, vals_list, strict=False):
                vals["name"] = _("%s (copy)", attribute.name)
        return vals_list
