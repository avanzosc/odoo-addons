# Copyright 2022 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartnerImport(models.Model):
    _inherit = "res.partner.import"

    def _get_line_values(self, row_values=False):
        self.ensure_one()
        values = super()._get_line_values(row_values=row_values)
        if row_values:
            partner_farm_numexp = row_values.get("Rega", "")
            partner_distance = row_values.get("Distance", "")
            values.update(
                {
                    "partner_farm_numexp": partner_farm_numexp,
                    "partner_distance": partner_distance,
                }
            )
        return values


class ResPartnerImportLine(models.Model):
    _inherit = "res.partner.import.line"

    partner_farm_numexp = fields.Char(
        string="Rega",
        states={"done": [("readonly", True)]},
        copy=False,
    )
    partner_distance = fields.Float(
        string="Distance",
        states={"done": [("readonly", True)]},
        copy=False,
    )

    def _partner_values(self):
        values = super()._partner_values()
        values.update(
            {
                "distance": self.partner_distance or self.partner_id.distance,
                "farm_numexp": self.partner_farm_numexp or self.partner_id.farm_numexp,
            }
        )
        return values
