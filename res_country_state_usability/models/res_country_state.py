# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResCountryState(models.Model):
    _inherit = "res.country.state"

    active = fields.Boolean(
        string="Active",
        default=True,
        help="Set active to false to hide the state without removing it.")

    def write(self, vals):
        res = super(ResCountryState, self).write(vals) if vals else True
        if "active" in vals and vals["active"]:
            # unarchiving a state does it on its country, too
            self.with_context(active_test=False).mapped("country_id").write(
                {"active": vals["active"]})
        return res

