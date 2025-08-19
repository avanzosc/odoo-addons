# Copyright 2025 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class SacaLine(models.Model):
    _inherit = "saca.line"

    rvd_number = fields.Char(
        string="RVD No.",
        help="Responsible Veterinary Declaration (RVD) Number",
        default=lambda self: self.env.company.rvd_number,
    )

    @api.onchange("company_id")
    def _onchange_company_rvd(self):
        for record in self:
            record.rvd_number = record.company_id.rvd_number
