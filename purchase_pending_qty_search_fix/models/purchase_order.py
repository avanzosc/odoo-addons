from odoo import _, api, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.model
    def _search_pending_qty_to_receive(self, operator, value):
        if operator not in ("=", "!=") or not isinstance(value, bool):
            raise ValueError(_("Unsupported search operator"))

        if operator == "!=":
            value = not value

        po_lines = self.env["purchase.order.line"].search(
            [("qty_to_receive", ">", 0.0)]
        )
        orders = po_lines.mapped("order_id")

        return [("id", "in", orders.ids)] if value else [("id", "not in", orders.ids)]
