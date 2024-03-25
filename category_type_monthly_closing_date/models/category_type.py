# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class CategoryType(models.Model):
    _inherit = "category.type"

    monthly_closing_date = fields.Date(string="Monthly Closing Date")
