# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models, fields


class ProductProduct(models.Model):
    _inherit = "product.product"

    last_purchase_price_company_currency = fields.Float(
        compute="_compute_last_purchase_price_currency",
        string="LPP in company currency"
    )
    last_purchase_price = fields.Float(
        string="LPP"
    )
    last_purchase_currency_id = fields.Many2one(
        string="LPP Currency",
    )
    last_purchase_price_currency = fields.Float(
        string="LPP Badge",
    )

    @api.depends(
        "last_purchase_line_id",
        "show_last_purchase_price_currency",
        "last_purchase_currency_id",
        "last_purchase_date",
    )
    def _compute_last_purchase_price_currency(self):
        result = super(
            ProductProduct, self)._compute_last_purchase_price_currency()
        for item in self:
            last_purchase_price_currency = 1
            if item.show_last_purchase_price_currency:
                rates = item.last_purchase_currency_id._get_rates(
                    item.last_purchase_line_id.company_id, item.last_purchase_date
                )
                last_purchase_price_currency = rates.get(
                    item.last_purchase_currency_id.id
                )
            item.last_purchase_price_company_currency = (
                item.last_purchase_line_id.price_unit /
                last_purchase_price_currency)
        return result
