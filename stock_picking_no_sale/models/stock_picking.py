from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    origin_not_exists = fields.Boolean(
        string="Missing Origin",
        compute="_compute_origin_not_exists",
        store=True,
    )

    @api.depends("origin")
    def _compute_origin_not_exists(self):
        sale_obj = self.env["sale.order"]
        purchase_obj = self.env["purchase.order"]
        for picking in self:
            if not picking.origin:
                picking.origin_not_exists = False
                continue
            origin_name = picking.origin
            has_sale = sale_obj.search_count([("name", "=", origin_name)]) > 0
            has_purchase = purchase_obj.search_count([("name", "=", origin_name)]) > 0
            picking.origin_not_exists = not (has_sale or has_purchase)
