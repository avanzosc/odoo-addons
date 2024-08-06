# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    product_brand_code = fields.Char(
        compute="_compute_brand_info",
        store=True,
        copy=False,
    )
    brand_fabricators = fields.Char(
        compute="_compute_brand_info",
        store=True,
        copy=False,
    )

    @api.depends(
        "product_id",
        "product_id.product_tmpl_id",
        "product_id.product_tmpl_id.seller_ids",
        "product_id.product_tmpl_id.seller_ids.partner_id",
        "product_id.product_tmpl_id.seller_ids.product_brand_id",
        "product_id.product_tmpl_id.seller_ids.product_brand_id.code",
        "product_id.product_tmpl_id.seller_ids.product_brand_id",
    )
    def _compute_brand_info(self):
        for move in self:
            product_brand_code = ""
            brand_fabricators = ""
            if move.product_id:
                sellers = move.product_id.seller_ids.filtered(
                    lambda x: x.product_brand_id and x.product_brand_id.code
                )
                for seller in sellers:
                    brand_code = seller.product_brand_id.code
                    product_brand_code = (
                        brand_code
                        if not product_brand_code
                        else "{}, {}".format(product_brand_code, brand_code)
                    )
                    partner_name = seller.partner_id.name
                    brand_fabricators = (
                        partner_name
                        if not brand_fabricators
                        else "{}, {}".format(brand_fabricators, partner_name)
                    )
            move.product_brand_code = product_brand_code
            move.brand_fabricators = brand_fabricators
