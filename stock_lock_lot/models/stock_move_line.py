from odoo import api, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    @api.model
    def create(self, vals):
        if vals.get("picking_type_id") and vals["picking_type_id"].create_lots:
            product = self.env["product.product"].browse(vals.get("product_id"))
            if product.tracking == "lot" and not vals.get("lot_name"):
                origin = (
                    vals.get("picking_id")
                    and self.env["stock.picking"].browse(vals["picking_id"]).origin
                    or ""
                )
                vals["lot_name"] = f"{vals['picking_id'].name}-{origin}"

        return super().create(vals)
