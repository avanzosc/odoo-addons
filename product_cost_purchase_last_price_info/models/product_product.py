# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    purchase_lines_ids = fields.One2many(
        string="Purchase lines",
        comodel_name="purchase.order.line",
        inverse_name="product_id",
        copy=False,
    )
    last_purchase_price_company_currency = fields.Float(
        compute="_compute_last_purchase_info",
        string="LPP in company currency",
        store=True,
        copy=False,
    )
    average_price_value = fields.Float(
        compute="_compute_average_price_value", string="Average price value"
    )
    last_purchase_value = fields.Float(
        compute="_compute_last_purchase_value", string="Last purchase value"
    )
    net_purchase_price = fields.Float(
        compute="_compute_net_purchase_price", string="Net purchase price"
    )

    @api.depends(
        "last_purchase_line_ids",
        "last_purchase_line_ids.state",
        "last_purchase_line_ids.price_unit",
        "last_purchase_line_ids.date_order",
        "last_purchase_line_ids.partner_id",
        "last_purchase_line_ids.currency_id",
    )
    def _compute_last_purchase_info(self):
        for product in self:
            product.last_purchase_price_company_currency = (
                product.last_purchase_price / product.last_purchase_price_currency
            )

    def _compute_average_price_value(self):
        for product in self:
            product.average_price_value = round(
                product.qty_available * product.standard_price, 2
            )

    def _compute_last_purchase_value(self):
        for product in self:
            product.last_purchase_value = product.qty_available * round(
                product.last_purchase_price_company_currency, 2
            )

    def _compute_net_purchase_price(self):
        for product in self:
            product.net_purchase_price = product.qty_available * round(
                product.last_purchase_net_unit_price, 2
            )
