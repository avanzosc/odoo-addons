# Copyright 2022 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class StockValuationLayer(models.Model):
    _inherit = "stock.valuation.layer"

    @api.model
    def _get_selection_valuation(self):
        return self.env["product.category"].fields_get(
            allfields=["property_valuation"]
        )["property_valuation"]["selection"]

    @api.model
    def _get_selection_cost_method(self):
        return self.env["product.category"].fields_get(
            allfields=["property_cost_method"]
        )["property_cost_method"]["selection"]

    valuation = fields.Selection(
        selection="_get_selection_valuation",
        string="Inventory Valuation",
    )
    cost_method = fields.Selection(
        selection="_get_selection_cost_method",
        string="Costing Method",
    )

    @api.model_create_multi
    def create(self, vals_list):
        product_model = self.env["product.product"]
        for vals in vals_list:
            if vals.get("cost_method") and vals.get("valuation"):
                continue
            product = product_model.browse(vals.get("product_id"))
            if not product:
                continue
            category = product.categ_id.with_company(vals.get("company_id"))
            if not vals.get("cost_method"):
                vals["cost_method"] = category.property_cost_method
            if not vals.get("valuation"):
                vals["valuation"] = category.property_valuation
        return super().create(vals_list)
