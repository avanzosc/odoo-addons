# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

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

    @api.depends("seller_ids")
    def _compute_main_seller(self):
        for product in self:
            seller = product.seller_ids[:1]
            product.main_seller_id = seller.partner_id
            product.main_seller_price = seller.price
