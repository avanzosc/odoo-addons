# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    treasury_margin_calculation = fields.Selection(
        selection=[
            ("cost", "Margin on Cost Price"),
            ("sale", "Margin on Sale Price"),
        ],
        default="cost",
        required=True,
        help=(
            "Choose how the sale price is calculated from the cost price "
            "and the margin.\n\n"
            "Margin on Cost Price:\n"
            "Sale Price = Cost Price * (1 + Margin / 100)\n"
            "Example: Cost 100, Margin 20% -> Sale Price 120.\n\n"
            "Margin on Sale Price:\n"
            "Sale Price = Cost Price / (1 - Margin / 100)\n"
            "Example: Cost 100, Margin 20% -> Sale Price 125.\n\n"
            "This calculation applies to treasury forecasts linked "
            "to a project when the category type is 'Both'."
        ),
    )
