# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    pricelist_price = fields.Float(
        string="Pricelist Price",
        compute="_compute_pricelist_price",
        digits="Product Price",
    )

    def _compute_pricelist_price(self):
        for product in self:
            price = 0
            if "pricelist_id" in self.env.context:
                price = product.with_context(
                    pricelist=self.env.context["pricelist_id"],
                    date=fields.Date.today()
                ).price
            product.pricelist_price = price
