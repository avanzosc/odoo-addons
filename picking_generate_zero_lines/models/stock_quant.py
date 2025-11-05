from odoo import api, models
from odoo.tools.float_utils import float_is_zero


class StockQuant(models.Model):
    _inherit = "stock.quant"

    @api.model
    def create(self, vals):
        qty = vals.get("quantity", 0.0)
        product_id = vals.get("product_id")
        if product_id:
            product = self.env["product.product"].browse(product_id)
            rounding = product.uom_id.rounding
            if float_is_zero(qty, precision_rounding=rounding):
                return self.env["stock.quant"]
        return super().create(vals)
