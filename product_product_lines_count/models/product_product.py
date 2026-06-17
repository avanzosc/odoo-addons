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
    stock_moves_count = fields.Integer(
        string="# Stock Moves",
        compute="_compute_stock_moves_count",
        store=True
    )    
    stock_move_lines_ids = fields.One2many(
        string="Stock Move Lines",
        comodel_name="stock.inventory.line",
        inverse_name="product_id"
    )
    stock_move_lines_count = fields.Integer(
        string="# Stock Moves Lines",
        compute="_compute_stock_moves_lines_count",
        store=True
    )
    stock_quants_count = fields.Integer(
        string="# Stock Quants",
        compute="_compute_stock_quants_count",
        store=True
    )    
    inventory_lines_ids = fields.One2many(
        string="Inventory Lines",
        comodel_name="stock.inventory.line",
        inverse_name="product_id"
    )
    inventory_lines_count = fields.Integer(
        string="# Inventory Lines",
        compute="_compute_inventory_lines_count",
        store=True
    )
    attributes_combination = fields.Char(
        string="Attribute Combination",
        compute="_compute_attribute_combination",
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

    @api.depends("stock_move_ids")
    def _compute_stock_moves_count(self):
        for product in self:
            product.stock_moves_count = len(product.stock_move_ids)

    @api.depends("stock_move_lines_ids")
    def _compute_stock_moves_lines_count(self):
        for product in self:
            product.stock_move_lines_count = len(product.stock_move_lines_ids)

    @api.depends("stock_quant_ids")
    def _compute_stock_quants_count(self):
        for product in self:
            product.stock_quants_count = len(product.stock_quant_ids)

    @api.depends("inventory_lines_ids")
    def _compute_inventory_lines_count(self):
        for product in self:
            product.inventory_lines_count = len(product.inventory_lines_ids)

    @api.depends("attribute_value_ids")
    def _compute_attribute_combination(self):
        for product in self:
            attributes = product.attribute_value_ids.sorted(key=lambda r: r.id)
            if not attributes:
                product.attributes_combination = ""
            else:
                product.attributes_combination =  f"({', '.join(map(str, attributes.ids))})"
