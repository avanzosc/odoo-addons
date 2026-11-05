# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class IrSequence(models.Model):
    _inherit = "ir.sequence"

    def _get_prefix_suffix(self, date=None, date_range=None):
        prefix, suffix = super()._get_prefix_suffix(date=date, date_range=date_range)
        if self.env.company.include_attributes and self.env.context.get(
            "attributes_code"
        ):
            prefix += self.env.context["attributes_code"].rjust(9, "0")
        return prefix, suffix
