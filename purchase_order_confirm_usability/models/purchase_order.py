# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
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
            purchase.picking_done = False
            if (purchase.picking_ids) and any(
                [picking.state == ("done") for picking in purchase.picking_ids]
            ):
                purchase.picking_done = True

    def button_confirm_pickings(self):
        for purchase in self:
            purchase.button_confirm()
            for purchase_line in purchase.order_line:
                if (
                    purchase_line.product_id
                    and (purchase_line.tracking != "none")
                    and not (purchase_line.lot_id)
                ):
                    raise ValidationError(
                        _("The product {} has not lot").format(
                            purchase_line.product_id.name
                        )
                    )
            for picking in purchase.picking_ids:
                picking.do_unreserve()
                picking.button_force_done_detailed_operations()
                for line in picking.move_line_ids_without_package:
                    if line.product_id:
                        line.lot_id = line.move_id.purchase_line_id.lot_id.id
                        line.qty_done = line.move_id.purchase_line_id.product_uom_qty
                res = picking.button_validate()
                return res
