# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    @api.onchange("product_qty", "product_uom", "company_id")
    def _onchange_quantity(self):
        result = {}
        parent_onchange = getattr(super(), "_onchange_quantity", None)
        if parent_onchange:
            result = parent_onchange()
        for line in self:
            rounding = line.product_uom.rounding if line.product_uom else 0.01
            if (
                line.qty_received
                and float_compare(
                    line.product_qty,
                    line.qty_received,
                    precision_rounding=rounding,
                )
                < 0
            ):
                raise UserError(
                    _(
                        "You cannot decrease the ordered quantity below the received"
                        " quantity."
                    )
                )
        return result

    def write(self, values):
        lines_to_update_picking = self.env["purchase.order.line"]
        if "product_qty" in values:
            for line in self:
                rounding = line.product_uom.rounding if line.product_uom else 0.01
                if (
                    float_compare(
                        values["product_qty"],
                        line.product_qty,
                        precision_rounding=rounding,
                    )
                    < 0
                ):
                    lines_to_update_picking |= line
        result = super().write(values)
        if lines_to_update_picking:
            lines_to_update_picking._put_new_qty_in_picking()
        return result

    def _put_new_qty_in_picking(self):
        for line in self:
            qty_in_picking = line.product_qty - line.qty_received
            line_product = line.product_id
            move = line.move_ids.filtered(
                lambda m, product=line_product: (
                    m.state == "assigned" and m.product_id == product
                )
            )
            if len(move) == 1:
                move.product_uom_qty = qty_in_picking
