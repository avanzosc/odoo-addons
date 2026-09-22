# Copyright 2025 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResCompany(models.Model):
    _inherit = "res.company"

    rvd_number = fields.Char(
        string="RVD No.",
        help="Responsible Veterinary Declaration (RVD) Number",
    )

    @api.constrains("rvd_number")
    def _check_rvd_number(self):
        for record in self.filtered("rvd_number"):
            if len(record.rvd_number) != 12 or not record.rvd_number.isdigit():
                raise ValidationError(
                    _("The RVD number must contain exactly 12 numeric digits.")
                )
