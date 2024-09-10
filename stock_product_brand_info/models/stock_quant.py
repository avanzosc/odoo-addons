# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class StockQuant(models.Model):
    _inherit = "stock.quant"

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
    brand_fabricator_id = fields.Many2one(
        "res.partner",
        string="Brand Fabricator",
        compute="_compute_brand_fabricator",
        store=True,
        copy=False,
    )

    @api.depends("product_id")
    def _compute_brand_fabricator(self):
        for quant in self:
            if quant.product_id:
                sellers = quant.product_id.seller_ids.filtered(
                    lambda x: x.product_brand_id and x.product_brand_id.code
                )
                if sellers:
                    quant.brand_fabricator_id = sellers[0].partner_id
                else:
                    quant.brand_fabricator_id = False

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
        for quant in self:
            product_brand_code = ""
            brand_fabricators = ""
            if quant.product_id:
                sellers = quant.product_id.seller_ids.filtered(
                    lambda x: x.product_brand_id and x.product_brand_id.code
                )
                if quant.brand_fabricator_id:
                    sellers = sellers.filtered(
                        lambda x: x.partner_id == quant.brand_fabricator_id
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
            quant.product_brand_code = product_brand_code
            quant.brand_fabricators = brand_fabricators
