# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.fields import Command


class ProductTemplate(models.Model):
    _inherit = "product.template"

    company_ids = fields.Many2many(
        string="Companies",
        comodel_name="res.company",
        relation="rel_product_companies",
        column1="product_id",
        column2="company_id",
    )

    @api.onchange("company_ids")
    def _onchange_company_ids(self):
        self.ensure_one()
        if len(self.company_ids) == 1:
            self.company_id = self.company_ids[:1].id
        else:
            self.company_id = False

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
