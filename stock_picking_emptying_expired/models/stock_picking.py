# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from datetime import datetime, timedelta

from odoo import _, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare


class StockPicking(models.Model):
    _inherit = "stock.picking"

    expiration_operation = fields.Boolean(
        string="Is Expiration Operation",
        default=False,
        related="picking_type_id.expiration_operation",
        store=True,
    )
    expired_date = fields.Date(
        string="Expired Date", default=lambda self: fields.Date.context_today(self)
    )

    def action_emptying_expired(self):
        move_obj = self.env["stock.move"]
        move_line_obj = self.env["stock.move.line"]
        expiration_products = self.env["product.product"].search(
            [("use_expiration_date", "=", True)]
        )
        for picking in self:
            if not picking.expired_date:
                raise ValidationError(_("You must enter the expired date."))
            for product in expiration_products:
                time = product.expiration_time
                date = picking.expired_date - timedelta(days=time)
                date_stock = product.with_context(
                    to_date=datetime.combine(date, datetime.max.time()),
                    location=picking.location_id.id,
                ).qty_available
                out_ml = move_line_obj.search(
                    [
                        ("product_id", "=", product.id),
                        ("location_id", "=", picking.location_id.id),
                        ("state", "=", "done"),
                    ]
                )
                out_ml = out_ml.filtered(
                    lambda l: date < l.date.date() <= picking.expired_date
                )
                out_qty = sum(out_ml.mapped("qty_done"))
                dif = date_stock - out_qty
                if (
                    float_compare(dif, 0.0, precision_rounding=product.uom_id.rounding)
                    > 0.0
                ):
                    move_obj.create(
                        {
                            "picking_id": picking.id,
                            "location_id": picking.location_id.id,
                            "location_dest_id": picking.location_dest_id.id,
                            "name": product.partner_ref,
                            "product_id": product.id,
                            "product_uom": product.uom_id.id,
                            "product_uom_qty": dif,
                        }
                    )
            picking.action_confirm()
            if picking.state != "assigned":
                picking.action_assign()
            if picking.state in ("waiting", "confirmed", "assigned"):
                picking.button_force_done_detailed_operations()
