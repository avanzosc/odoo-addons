# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    update_line_qty = fields.Boolean(
        string="Update Order Lines Qty",
        default=False,
        copy=False,
    )

    def button_return_picking(self):
        self.update_line_qty = True
        return super().button_return_picking()
