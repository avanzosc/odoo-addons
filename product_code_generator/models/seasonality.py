# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class Seasonality(models.Model):
    _inherit = "seasonality"

    code = fields.Char(
        size=3,
        required=True,
        default="000",
        help="3-digit code used as the season segment of the "
        "automatically generated product reference.",
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("code"):
                vals["code"] = vals["code"].rjust(3, "0")
        return super().create(vals_list)

    def write(self, vals):
        if vals.get("code"):
            vals["code"] = vals["code"].rjust(3, "0")
        return super().write(vals)
