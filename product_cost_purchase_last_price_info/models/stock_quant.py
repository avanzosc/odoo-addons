# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models, fields


class StockQuant(models.Model):
    _inherit = "stock.quant"

    last_purchase_price_company_currency = fields.Float(
        string="LPP in company currency",
        related="product_id.last_purchase_price_company_currency",
        groups="stock.group_stock_manager"
    )
    purchase_value = fields.Monetary(
        compute="_compute_purchase_value", string="Purchase Value",
        groups="stock.group_stock_manager"
    )
    standard_price = fields.Float(
        string="Product Price",
        compute="_compute_standard_price",
        groups="stock.group_stock_manager"
    )

    def _compute_purchase_value(self):
        for quant in self:
            if not quant.location_id:
                quant.purchase_value = 0
                return
            if not quant.location_id._should_be_valued() or\
                    (quant.owner_id and quant.owner_id != quant.company_id.partner_id):
                quant.sudo().purchase_value = 0
                continue
            quant.sudo().purchase_value = (
                quant.quantity *
                quant.product_id.last_purchase_price_company_currency)

    def _compute_standard_price(self):
        for quant in self:
            if quant.product_id:
                quant.sudo().standard_price = (
                    quant.quantity * quant.product_id.standard_price)
            else:
                quant.sudo().standard_price = 0
