from odoo import _, api, models
from odoo.exceptions import UserError


class StockQuant(models.Model):
    _inherit = "stock.quant"

    @api.model
    def create(self, vals):
        product = self.env["product.product"].browse(vals.get("product_id"))
        if product.tracking != "none" and not vals.get("lot_id"):
            raise UserError(
                _("Cannot create quant for a traceable " "product without a lot.")
            )
        return super().create(vals)
