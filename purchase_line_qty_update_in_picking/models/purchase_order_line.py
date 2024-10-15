# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, models
from odoo.exceptions import UserError


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    @api.onchange("product_qty", "product_uom", "company_id")
    def _onchange_quantity(self):
        result = super(PurchaseOrderLine, self)._onchange_quantity()
        if self.qty_received and self.product_qty < self.qty_received:
            raise UserError(_("Amount less than amount received."))
        return result

    def write(self, values):
        found = False
        if (
            len(self) == 1
            and "product_qty" in values
            and values.get("produt_qty", 0.0) < self.product_qty
        ):
            found = True
        result = super(PurchaseOrderLine, self).write(values)
        if found:
            self._put_new_qty_in_picking()
        return result

    def _put_new_qty_in_picking(self):
        qty_in_picking = self.product_qty - self.qty_received
        move = self.move_ids.filtered(lambda x: x.state == "assigned")
        if len(move) == 1:
            move.product_uom_qty = qty_in_picking
