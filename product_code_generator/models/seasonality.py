# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import  ValidationError


class Seasonality(models.Model):
    _inherit = "seasonality"

    code = fields.Char(
        size=3,
        required=True,
        default="000",
        help="3-digit code used as the season segment of the "
        "automatically generated product reference.",
    )

    @api.constrains('code')
    def _check_code_size(self):
        for record in self:
            if record.code and len(record.code) != 3:
                raise ValidationError(_("Code must be 3-character long. Please enter a correct one."))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals["code"] = vals["code"].rjust(3, "0")
        return super().create(vals_list)

    def write(self, vals):
        if "code" in vals:
            vals["code"] = vals["code"].rjust(3, "0")
        return super().write(vals)
