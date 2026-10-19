# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    last_supplier_move_date = fields.Date(
        string="Last supplier move date",
    )
    last_supplier_move_price = fields.Float(string="Last supplier move price")
    last_supplier_move_id = fields.Many2one(
        comodel_name="res.partner",
        string="Last supplier move",
    )

    def _found_invoice_supplier_last_line(self):
        if not self.check_access_rights("write", raise_exception=False):
            return
        cond = [
            ("product_id", "=", self.id),
            ("move_id.move_type", "=", "in_invoice"),
            ("move_id.state", "=", "posted"),
            ("display_type", "=", "product"),
            ("price_subtotal", ">", 0),
            ("quantity", ">", 0),
        ]
        last_line = self.env["account.move.line"].search(
            cond, order="date desc", limit=1
        )
        return last_line

    def _assign_values_last_invoice_info(self, last_line):
        if last_line:
            vals = {
                "last_supplier_move_date": last_line.move_id.invoice_date,
                "last_supplier_move_price": last_line.price_unit,
                "last_supplier_move_id": last_line.move_id.partner_id.id,
            }
        else:
            vals = {
                "last_supplier_move_date": False,
                "last_supplier_move_price": 0,
                "last_supplier_move_id": False,
            }
        return vals

    def _update_invoice_supplier_last_info(self, vals):
        self.write(vals)
        if len(self.product_tmpl_id) == 1:
            self.product_tmpl_id.write(vals)
