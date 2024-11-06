from odoo import api, fields, models


class StockReplenishment(models.Model):
    _inherit = "stock.warehouse.orderpoint"

    qty_in_kits = fields.Float(
        string="Qty Kit",
        compute="_compute_qty_in_kits",
        readonly=True,
        store=True,
    )

    count_component_kit = fields.Integer(
        compute="_compute_count_component_kit",
        readonly=True,
        store=True,
    )

    @api.depends("product_id", "product_id.product_tmpl_id.basket_lines")
    def _compute_qty_in_kits(self):
        for orderpoint in self:
            product = orderpoint.product_id
            qty_in_kits = 0.0

            for bom_line in product.basket_lines:
                parent_product_tmpl = bom_line.bom_id.product_tmpl_id

                sale_order_lines = self.env["sale.order.line"].search(
                    [
                        ("product_id.product_tmpl_id", "=", parent_product_tmpl.id),
                        ("order_id.state", "in", ["draft", "sent"]),
                    ]
                )

                total_sale_line_qty = sum(sale_order_lines.mapped("product_uom_qty"))
                qty_in_kits += total_sale_line_qty * bom_line.product_qty

            orderpoint.qty_in_kits = qty_in_kits

    @api.depends("product_id", "product_id.product_tmpl_id.basket_lines")
    def _compute_count_component_kit(self):
        for orderpoint in self:
            product = orderpoint.product_id
            orderpoint.count_component_kit = len(product.basket_lines)

    def button_calculate_qty_in_kits(self):
        self._compute_qty_in_kits()
        return True

    def button_assign_qty_in_orderpoint(self):
        for orderpoint in self:
            qty_to_order = (
                orderpoint.qty_in_kits
                + orderpoint.outgoing_qty2
                + orderpoint.outgoing_qty
                - (
                    orderpoint.qty_on_hand
                    + orderpoint.incoming_qty
                    + orderpoint.incoming_qty2
                )
            )
            orderpoint.qty_to_order = qty_to_order
