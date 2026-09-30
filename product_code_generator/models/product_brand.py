# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductBrand(models.Model):
    _inherit = "product.brand"

    code = fields.Char(
        size=2,
        required=True,
        default="00",
        help="2-digit code used as the brand segment of the automatically "
        "generated product reference.",
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("code"):
                vals["code"] = vals["code"].rjust(2, "0")
        return super().create(vals_list)

    def write(self, vals):
        if vals.get("code"):
            vals["code"] = vals["code"].rjust(2, "0")
        return super().write(vals)
