# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, models, fields


class ProductProduct(models.Model):
    _inherit = "product.product"
    
    sale_lines_ids = fields.One2many(
        string="Sale Lines",
        comodel_name="sale.order.line",
        inverse_name="product_id"
    )
    sale_lines_count = fields.Integer(
        string="# Sale Lines",
        compute="_compute_sale_lines_count",
        store=True
    )
    purchase_lines_ids = fields.One2many(
        string="Purchase Lines",
        comodel_name="purchase.order.line",
        inverse_name="product_id"
    )
    purchase_lines_count = fields.Integer(
        string="# Purchase Lines",
        compute="_compute_purchase_lines_count",
        store=True
    )
    invoice_lines_ids = fields.One2many(
        string="Invoice Lines",
        comodel_name="account.invoice.line",
        inverse_name="product_id"
    )
    invoice_lines_count = fields.Integer(
        string="# Invoice Lines",
        compute="_compute_invoice_lines_count",
        store=True
    )

    @api.depends("sale_lines_ids")
    def _compute_sale_lines_count(self):
        for product in self:
            product.sale_lines_count = len(product.sale_lines_ids)

    @api.depends("purchase_lines_ids")
    def _compute_purchase_lines_count(self):
        for product in self:
            product.purchase_lines_count = len(product.purchase_lines_ids)

    @api.depends("invoice_lines_ids")
    def _compute_invoice_lines_count(self):
        for product in self:
            product.invoice_lines_count = len(product.invoice_lines_ids)
