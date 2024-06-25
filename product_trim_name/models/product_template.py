# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import unicodedata

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    trim_name = fields.Char(
        string="Trim Name", compute="_compute_trim_name", store=True
    )

    @api.depends("name")
    def _compute_trim_name(self):
        for product in self:
            trim_name = product.name.replace(" ", "")
            trim_name = "".join(
                c
                for c in unicodedata.normalize("NFD", trim_name)
                if unicodedata.category(c) != "Mn"
            )
            product.trim_name = trim_name
