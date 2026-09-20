from odoo import _, fields, models
from odoo.exceptions import UserError


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    product_discount_percentage = fields.Float(
        related="product_id.discount_percentage",
    )
    product_exclude_discount_categ = fields.Boolean(
        related="product_id.categ_id.discounts_exclude",
    )

    def recalculate_invoice_line(self):
        for line in self:
            move = line.move_id
            if move.state != "draft":
                raise UserError(_("You can only recalculate draft invoice lines."))
            discount_percentage = line.product_discount_percentage
            if not line.product_exclude_discount_categ or not discount_percentage:
                continue
            subtotal = sum(
                move.invoice_line_ids.filtered(
                    lambda invoice_line: (
                        invoice_line.display_type == "product"
                        and not invoice_line.product_id.categ_id.discounts_exclude
                        and not invoice_line.product_id.discount_percentage
                    )
                ).mapped("price_subtotal")
            )
            line.price_unit = subtotal * (discount_percentage / 100) * -1
        return True
