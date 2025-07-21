# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    last_supplier_move_date = fields.Date(
        string="Last supplier move date",
    )
    last_supplier_move_price = fields.Float(
        string="Last supplier move price",
        digits="Product Price",
    )
    last_supplier_move_id = fields.Many2one(
        comodel_name="res.partner",
        string="Last supplier move",
    )
    last_supplier_move_discount = fields.Float(
        string="Last Supplier Move Discount (%)",
        digits="Discount",
        default=0.0,
        copy=False,
    )
    last_supplier_move_net_unit_price = fields.Float(default=0.0, copy=False)

    def set_product_last_supplier_move(self, move_id=False):
        move_line_obj = self.env["account.move.line"]
        if not self.check_access_rights("write", raise_exception=False):
            return
        for product in self:
            last_supplier_move_date = False
            last_supplier_move_price = 0.0
            last_supplier_move_id = False
            last_supplier_move_discount = 0.0
            last_supplier_move_net_unit_price = 0.0
            if move_id:
                cond = [
                    ("move_id", "=", move_id),
                    ("product_id", "=", product.id),
                    ("display_type", "=", "product"),
                    ("price_subtotal", ">", 0),
                    ("quantity", ">", 0),
                ]
                lines = move_line_obj.search(cond, limit=1)
            else:
                cond = [
                    ("product_id", "=", product.id),
                    ("move_id.move_type", "=", "in_invoice"),
                    ("move_id.state", "not in", ["draft", "cancel"]),
                    ("display_type", "=", "product"),
                    ("price_subtotal", ">", 0),
                    ("quantity", ">", 0),
                ]
                lines = move_line_obj.search(cond).sorted(
                    key=lambda ln: ln.move_id.invoice_date, reverse=True
                )
            if lines:
                last_line = lines[:1]
                last_supplier_move_date = last_line.move_id.invoice_date
                last_supplier_move_price = product.uom_id._compute_quantity(
                    last_line.price_unit, last_line.product_uom_id
                )
                last_supplier_move_id = last_line.move_id.partner_id
                last_supplier_move_discount = last_line.discount
                last_supplier_move_net_unit_price = (
                    last_line.price_subtotal / last_line.quantity
                )
            product.write(
                {
                    "last_supplier_move_date": last_supplier_move_date,
                    "last_supplier_move_price": last_supplier_move_price,
                    "last_supplier_move_id": (
                        last_supplier_move_id.id if last_supplier_move_id else False
                    ),
                    "last_supplier_move_discount": last_supplier_move_discount,
                    "last_supplier_move_net_unit_price": last_supplier_move_net_unit_price,
                }
            )
            if len(product.product_tmpl_id) == 1:
                product.product_tmpl_id.set_product_template_last_purchase_move(
                    last_supplier_move_date,
                    last_supplier_move_price,
                    last_supplier_move_id,
                    last_supplier_move_discount,
                    last_supplier_move_net_unit_price,
                )
