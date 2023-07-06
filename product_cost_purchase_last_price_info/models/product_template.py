# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    last_purchase_price_company_currency = fields.Float(
        compute="_compute_last_purchase_price_company_currency",
        string="LPP in company currency", store=True, copy=False
    )
    average_price_value = fields.Float(
        compute="_compute_average_price_value",
        string="Average price value"
    )
    last_purchase_value = fields.Float(
        compute="_compute_last_purchase_value",
        string="Last purchase value"
    )

    @api.depends("product_variant_ids",
                 "product_variant_ids.last_purchase_price_company_currency")
    def _compute_last_purchase_price_company_currency(self):
        for template in self:
            last_purchase_price_company_currency = 0
            if template.product_variant_ids:
                variant = template.product_variant_ids[0]
                last_purchase_price_company_currency = (
                    variant.last_purchase_price_company_currency)
            template.last_purchase_price_company_currency = (
                last_purchase_price_company_currency)

    def _compute_average_price_value(self):
        for template in self:
            template.average_price_value = (
                template.qty_available * template.standard_price)

    def _compute_last_purchase_value(self):
        for template in self:
            last_purchase_value = 0
            if len(template.product_variant_ids) == 1:
                variant = template.product_variant_ids[0]
                last_purchase_value = (
                    template.qty_available *
                    round(variant.last_purchase_price_company_currency, 2))
            template.last_purchase_value = last_purchase_value
