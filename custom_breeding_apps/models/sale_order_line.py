# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    product_category_id = fields.Many2one(
        string="Product Category",
        comodel_name="product.category",
        related="product_id.categ_id",
        store=True,
    )
    partner_shipping_id = fields.Many2one(
        string="Partner Shipping",
        comodel_name="res.partner",
        related="order_id.partner_shipping_id",
        store=True,
    )
    packaging_name = fields.Char(
        string="Packaging N.", related="product_packaging.name", store=True
    )
    entire_chick_percentage = fields.Float(
        string="Entire Chicks", compute="_compute_entire_chick_percentage", store=True
    )

    @api.depends("product_id", "product_id.entire_chick_percentage", "product_uom_qty")
    def _compute_entire_chick_percentage(self):
        for line in self:
            qty = 0
            if line.product_id and line.product_id.entire_chick_percentage:
                qty = line.product_uom_qty / (line.product_id.entire_chick_percentage)
            line.entire_chick_percentage = qty

    def _check_package(self):
        result = super()._check_package()
        if "warning" in result:
            result = {}
        return result
