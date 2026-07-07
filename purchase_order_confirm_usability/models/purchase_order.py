# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    picking_done = fields.Boolean(
        string="Pickings are done", compute="_compute_picking_done", store=True
    )

    @api.depends("picking_ids", "picking_ids.state")
    def _compute_picking_done(self):
        for purchase in self:
            purchase.picking_done = bool(purchase.picking_ids) and any(
                picking.state == "done" for picking in purchase.picking_ids
            )

    def button_confirm_pickings(self):
        result = False
        for purchase in self:
            purchase.button_confirm()
            for purchase_line in purchase.order_line:
                if (
                    purchase_line.product_id
                    and purchase_line.tracking != "none"
                    and not purchase_line.lot_id
                ):
                    raise ValidationError(
                        _("The product {} has not lot").format(
                            purchase_line.product_id.name
                        )
                    )
            for picking in purchase.picking_ids:
                picking.do_unreserve()
                picking.button_force_done_detailed_operations()
                picking.custom_date_done = purchase.date_planned
                for line in picking.move_line_ids_without_package:
                    if line.product_id:
                        line.lot_id = line.move_id.purchase_line_id.lot_id
                        line.quantity = line.move_id.purchase_line_id.product_uom_qty
                result = picking.button_validate()
        return result
