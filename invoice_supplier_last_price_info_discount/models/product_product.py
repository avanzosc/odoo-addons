# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    last_supplier_move_discount = fields.Float(
        string="Last Supplier Move Discount (%)",
        digits="Discount",
        default=0.0,
        copy=False,
    )
    last_supplier_move_net_unit_price = fields.Float(default=0.0, copy=False)

    def _assign_values_last_invoice_info(self, last_line):
        vals = super()._assign_values_last_invoice_info(last_line)
        if last_line:
            last_supplier_move_discount = last_line.discount if last_line else 0
            if last_line.discount:
                last_supplier_move_net_unit_price = last_line.price_unit - (
                    last_line.price_unit * (last_line.discount / 100)
                )
            else:
                last_supplier_move_net_unit_price = 0
            vals["last_supplier_move_discount"] = last_supplier_move_discount
            vals["last_supplier_move_net_unit_price"] = (
                last_supplier_move_net_unit_price
            )
        else:
            vals["last_supplier_move_discount"] = 0
            vals["last_supplier_move_net_unit_price"] = 0
        return vals
