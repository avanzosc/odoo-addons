# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    family_id = fields.Many2one(comodel_name="product.category")
    sub_family_id = fields.Many2one(comodel_name="product.category", string="Subfamily")
    season_id = fields.Many2one(comodel_name="seasonality")

    @api.onchange("family_id", "sub_family_id")
    def _onchange_family(self):
        if self.family_id:
            self.categ_id = self.sub_family_id or self.family_id

    def generate_code(self):
        for template in self:
            template.product_variant_ids.generate_code()
