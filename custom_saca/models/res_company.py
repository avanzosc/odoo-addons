# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResCompany(models.Model):
    _inherit = "res.company"

    disinfectant_id = fields.Many2one(
        string="Disinfectant", comodel_name="product.product"
    )
    report = fields.Binary(string="Reports")
    rvd_number = fields.Char(
        string="RVD No.",
        size=12,
        help="Responsible Veterinary Declaration Number (12 digits)",
    )

    @api.constrains("rvd_number")
    def _check_rvd_number(self):
        for record in self:
            if record.rvd_number and (
                not record.rvd_number.isdigit() or len(record.rvd_number) != 12
            ):
                raise ValidationError(
                    _("The RVD number must contain exactly 12 numeric digits.")
                )
