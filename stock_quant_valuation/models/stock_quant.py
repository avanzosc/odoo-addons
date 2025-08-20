# Copyright 2025 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models, api

class StockQuant(models.Model):
    _inherit = "stock.quant"
    
    product_cost = fields.Float(
        string="Cost",
        related="product_id.standard_price",
        digits="Product Price",
        groups="stock.group_stock_manager",
    )
    
    lot_average_unit_price = fields.Float(
        string="Lot Average Unit Price",
        digits="Product Price",
        compute="_compute_lot_average_unit_price",
        groups="stock.group_stock_manager",
        help="If linked to a lot, takes the lot's average unit price. "
             "Otherwise, uses the product's last purchase price.",
    )
    
    lot_average_value = fields.Float(
        string="Lot Average Value",
        digits="Account",
        compute="_compute_lot_average_value",
        groups="stock.group_stock_manager",
        help="Quant quantity multiplied by the lot average unit price.",
    )

    lot_purchase_cost = fields.Float(
        string="Lot Purchase Cost",
        digits="Product Price",
        compute="_compute_lot_purchase_cost",
        groups="stock.group_stock_manager",
        help="If linked to a lot, takes the lot's purchase cost. "
             "Otherwise, uses the product's last purchase price.",
    )
    
    lot_purchase_value = fields.Float(
        string="Lot Purchase Value",
        digits="Account",
        compute="_compute_lot_purchase_value",
        groups="stock.group_stock_manager",
        help="Quant quantity multiplied by the lot purchase cost.",
    )
    
    @api.depends("lot_id", "product_id")
    def _compute_lot_average_unit_price(self):
        for quant in self:
            quant.lot_average_unit_price = (
                quant.lot_id.average_price
                if quant.lot_id
                else quant.product_id.last_purchase_price or 0.0
            )
            
    @api.depends("quantity", "lot_average_unit_price")   
    def _compute_lot_average_value(self):
        for quant in self:
            quant.lot_average_value = quant.quantity * quant.lot_average_unit_price  
            
    @api.depends("lot_id", "product_id")
    def _compute_lot_purchase_cost(self):
        for quant in self:
            quant.lot_purchase_cost = (
                quant.lot_id.purchase_cost
                if quant.lot_id
                else quant.product_id.last_purchase_price or 0.0
            )
            
    @api.depends("quantity", "lot_purchase_cost")   
    def _compute_lot_purchase_value(self):
        for quant in self:
            quant.lot_purchase_value = quant.quantity * quant.lot_purchase_cost
            
 
            