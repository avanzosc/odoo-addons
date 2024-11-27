# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from datetime import timedelta

from odoo import _, fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    update_line_qty = fields.Boolean(
        string="Update Order Lines Qty",
        default=False,
        copy=False,
    )

    def button_return_picking(self):
        self.update_line_qty = True
        return super().button_return_picking()

    def action_view_sale_lines(self):
        result = super().action_view_sale_lines()
        view_tree_id = self.env.ref("custom_p.view_sales_order_line_input_tree").id
        result["views"] = [(view_tree_id, "tree")]
        result["view"] = view_tree_id
        return result

    def action_last_month_partner_sales(self):
        self.ensure_one()
        if not self.partner_id:
            raise ValidationError(_("This sale has not partner."))
        else:
            now = fields.Datetime.now()
            last_month = now - timedelta(days=31)
            domain = [
                ("order_partner_id", "=", self.partner_id.id),
                ("state", "=", "sale"),
                ("date_order", ">=", last_month),
                ("product_uom_qty", ">", 0),
            ]
            sale_lines = self.env["sale.order.line"].search(domain)
            products = []
            for line in sale_lines:
                if line.product_id not in products:
                    products.append(line.product_id)
            for product in products:
                if product not in self.order_line.mapped("product_id"):
                    self.env["sale.order.line"].create(
                        {
                            "product_id": product.id,
                            "product_uom": product.uom_id.id,
                            "product_uom_qty": 0,
                            "order_id": self.id,
                        }
                    )
