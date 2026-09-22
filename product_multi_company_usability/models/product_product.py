# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models
from odoo.fields import Command


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)
        for line, vals in zip(lines, vals_list, strict=False):
            company_id = vals.get("company_id")
            if company_id:
                line.company_ids = [Command.link(company_id)]
        return lines

    def write(self, vals):
        result = super().write(vals)
        if "company_id" in vals and vals.get("company_id", False):
            for line in self.filtered("company_id"):
                line.company_ids = [Command.link(line.company_id.id)]
        return result
