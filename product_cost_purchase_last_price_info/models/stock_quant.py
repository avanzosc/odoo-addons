# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    last_purchase_price_company_currency = fields.Float(
        string="LPP in company currency",
        related="product_id.last_purchase_price_company_currency",
        groups="stock.group_stock_manager",
        store=True,
        copy=False,
    )
    purchase_value = fields.Monetary(
        compute="_compute_purchase_value",
        string="Last purchase price value",
        groups="stock.group_stock_manager",
        store=True,
        copy=False,
    )
    standard_price = fields.Float(
        string="Product Price",
        related="product_id.standard_price",
        store=True,
        copy=False,
        groups="stock.group_stock_manager",
    )
    value = fields.Monetary(string="Product cost price value")
    value_to_pivot = fields.Monetary(
        string="Product cost price value", related="value", store=True, copy=False
    )

    @api.depends(
        "location_id",
        "quantity",
        "product_id",
        "product_id.last_purchase_price_company_currency",
    )
    def _compute_purchase_value(self):
        for quant in self:
            if not quant.location_id:
                quant.purchase_value = 0
                return
            if not quant.location_id._should_be_valued() or (
                quant.owner_id and quant.owner_id != quant.company_id.partner_id
            ):
                quant.sudo().purchase_value = 0
                continue
            quant.sudo().purchase_value = quant.quantity * round(
                quant.product_id.last_purchase_price_company_currency, 2
            )
