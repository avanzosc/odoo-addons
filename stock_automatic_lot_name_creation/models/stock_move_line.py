from odoo import api, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            picking_id = vals.get("picking_id")
            product_id = vals.get("product_id")
            product = self.env["product.product"].browse(product_id)

            if product and product.tracking == "lot" and not vals.get("lot_name"):
                picking = self.env["stock.picking"].browse(picking_id)
                origin = picking.origin or ""
                vals["lot_name"] = f"{picking.name}-{origin}"

        return super().create(vals_list)
