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

    @api.model
    def create(self, values):
        product_id = values.get("product_id")
        company_id = values.get("company_id")
        if not values.get("cost_method", False):
            values.update(
                {
                    "cost_method": self.env["product.product"]
                    .browse(product_id)
                    .categ_id.with_company(company_id)
                    .property_cost_method,
                }
            )
        if not values.get("valuation", False):
            values.update(
                {
                    "valuation": self.env["product.product"]
                    .browse(product_id)
                    .categ_id.with_company(company_id)
                    .property_valuation,
                }
            )
        return super(StockValuationLayer, self).create(values)
