# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


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

    @api.model
    def create(self, values):
        line = super().create(values)
        if "company_id" in values and values.get("company_id", False):
            company = self.env["res.company"].browse(values.get("company_id"))
            line.company_ids = [(4, company.id)]
        return line

    def write(self, values):
        result = super().write(values)
        if "company_id" in values and values.get("company_id", False):
            for line in self:
                if line.company_id:
                    line.company_ids = [(4, line.company_id.id)]
        return result
