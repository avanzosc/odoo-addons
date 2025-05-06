# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    seller_id = fields.Many2one(
        string="Supplier Pricelist", comodel_name="product.supplierinfo", copy=False
    )
    product_seller_ids = fields.Many2many(
        string="Suppliers Pricelists",
        comodel_name="product.supplierinfo",
        compute="_compute_product_seller_ids",
    )

    @api.depends("product_id")
    def _compute_product_seller_ids(self):
        for line in self:
            sellers = self.env["product.supplierinfo"]
            if line.product_id and line.product_id.seller_ids:
                sellers = line.product_id.seller_ids
            line.product_seller_ids = [(6, 0, sellers.ids)]

    @api.onchange("seller_id")
    def onchange_seller_id(self):
        if self.seller_id:
            if self.seller_id.product_name:
                name = "[{}] {}".format(
                    self.seller_id.product_code, self.seller_id.product_name
                )
            else:
                name = "[{}] {}".format(
                    self.seller_id.product_code, self.product_id.name
                )
            self.name = name
            self.price_unit = self.seller_id.price
            self.discount = self.seller_id.discount
