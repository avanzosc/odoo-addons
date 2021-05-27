# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResCountry(models.Model):
    _inherit = "res.country"

    active = fields.Boolean(
        string="Active",
        default=True,
        help="Set active to false to hide the country without removing it.")

    def write(self, vals):
        res = super(ResCountry, self).write(vals) if vals else True
        if "active" in vals and not vals["active"]:
            # archiving a country does it on its states, too
            self.mapped(
                "state_ids").write(
                {"active": vals["active"]})
        return res
