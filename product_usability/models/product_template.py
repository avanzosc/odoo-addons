# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    consumed_last_twelve_months = fields.Float(
        digits="Product Unit of Measure",
        compute="_compute_consumed_last_twelve_months",
    )
    months_with_stock = fields.Integer(
        compute="_compute_months_with_stock",
    )
    main_seller_id = fields.Many2one(
        string="Main Seller",
        comodel_name="res.partner",
        compute="_compute_main_seller",
        store=True,
        copy=False,
    )
    main_seller_price = fields.Float(
        compute="_compute_main_seller",
        store=True,
        copy=False,
    )
    root_category_id = fields.Many2one(
        comodel_name="product.category",
        string="Root Category",
        related="categ_id.root_category_id",
        store=True,
    )
    parent_category_id = fields.Many2one(
        comodel_name="product.category",
        string="Parent Category",
        related="categ_id.parent_id",
        store=True,
    )

    def _compute_consumed_last_twelve_months(self):
        for template in self:
            consumed_last_twelve_months = 0
            if len(template.product_variant_ids) == 1:
                consumed_last_twelve_months = template.product_variant_ids[
                    0
                ].consumed_last_twelve_months
            template.consumed_last_twelve_months = consumed_last_twelve_months

    def _compute_months_with_stock(self):
        for template in self:
            months_with_stock = 0
            if len(template.product_variant_ids) == 1:
                months_with_stock = template.product_variant_ids[0].months_with_stock
            template.months_with_stock = months_with_stock

    @api.depends("seller_ids")
    def _compute_main_seller(self):
        for product in self:
            seller = product.seller_ids[:1]
            product.main_seller_id = seller.partner_id
            product.main_seller_price = seller.price
