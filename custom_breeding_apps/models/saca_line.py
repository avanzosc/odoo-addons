# Copyright 2025 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class SacaLine(models.Model):
    _inherit = "saca.line"

    rvd_number = fields.Char(
        string="RVD No.",
        help="Responsible Veterinary Declaration (RVD) Number",
        default=lambda self: self.env.company.rvd_number
        if not self.external_supplier
        else False,
    )

    @api.onchange("company_id")
    def _onchange_company_rvd(self):
        for record in self:
            if not self.external_supplier:
                record.rvd_number = record.company_id.rvd_number

    @api.onchange("external_supplier")
    def _onchange_external_supplier(self):
        for record in self:
            record.rvd_number = (
                False if self.external_supplier else record.company_id.rvd_number
            )
