# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models



class ProductProduct(models.Model):
    _inherit = "product.product"

    last_supplier_move_date = fields.Date(string="Last supplier move date")
    last_supplier_move_price = fields.Float(
        string="Last supplier move price", digits="Product Price"
    )
    last_supplier_move_id = fields.Many2one(
        comodel_name="res.partner", string="Last supplier move"
    )

    def set_product_last_supplier_move(self, move_id=False):
        move_line_obj = self.env["account.move.line"]
        if not self.check_access_rights("write", raise_exception=False):
            return
        for product in self:
            last_supplier_move_date = False
            last_supplier_move_price = 0.0
            last_supplier_move_id = False
            if move_id:
                cond = [
                    ("move_id", "=", move_id),
                    ("product_id", "=", product.id),
                ]
                lines = move_line_obj.search(cond, limit=1)
            else:
                cond = [
                    ("product_id", "=", product.id),
                    ("move_id.type", "=", "in_move"),
                    ("move_id.state", "not in", ["draft", "cancel"]),
                ]
                lines = move_line_obj.search(cond).sorted(
                    key=lambda l: l.move_id.date_move, reverse=True
                )
            if lines:
                last_line = lines[:1]
                last_supplier_move_date = last_line.move_id.date_move
                last_supplier_move_price = product.uom_id._compute_quantity(
                    last_line.price_unit, last_line.uom_id
                )
                last_supplier_move_id = last_line.move_id.partner_id
            product.write(
                {
                    "last_supplier_move_date": last_supplier_move_date,
                    "last_supplier_move_price": last_supplier_move_price,
                    "last_supplier_move_id": (
                        last_supplier_move_id.id
                        if last_supplier_move_id
                        else False
                    ),
                }
            )
            if len(product.product_tmpl_id) == 1:
                product.product_tmpl_id.set_product_template_last_purchase(
                    last_supplier_move_date,
                    last_supplier_move_price,
                    last_supplier_move_id,
                )
