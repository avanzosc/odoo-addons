from odoo import fields, models

class ProductQuarteringLocation(models.Model):
    _name = "product.quartering.location"
    _description = "Product Quartering Locations"
    _order = "product_final_id,position"   
    
    product_final_id = fields.Many2one(comodel_name="product.final", 
                                       string="Final Product")
    product_id = fields.Many2one(comodel_name="product.product")
    position = fields.Char(string="Position")
