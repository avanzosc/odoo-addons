# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    treasury_margin_calculation = fields.Selection(
        related="company_id.treasury_margin_calculation",
        readonly=False,
        string="Treasury Margin Calculation",
        help=(
            "Select the default margin calculation method for new projects.\n\n"
            "Margin on Cost Price:\n"
            "Sale Price = Cost Price * (1 + Margin / 100)\n"
            "Example: Cost 100, Margin 20% -> Sale Price 120.\n\n"
            "Margin on Sale Price:\n"
            "Sale Price = Cost Price / (1 - Margin / 100)\n"
            "Example: Cost 100, Margin 20% -> Sale Price 125."
        ),
    )
