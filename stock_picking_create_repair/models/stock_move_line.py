# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    created_repair_id = fields.Many2one(
        string="Created repair", comodel_name="repair.order", copy=False
    )
    sale_line_id = fields.Many2one(
        string="Sale line",
        comodel_name="sale.order.line",
        related="move_id.sale_line_id",
        store=True,
        copy=False,
    )
    is_repair = fields.Boolean(
        string="It's repair", store=True, copy=False, compute="_compute_is_repair"
    )
    picking_type_id = fields.Many2one(
        string="Operation Type",
        comodel_name="stock.picking.type",
        related="picking_id.picking_type_id",
        store=True,
        copy=False,
    )

    @api.depends("move_id", "move_id.is_repair")
    def _compute_is_repair(self):
        for line in self:
            line.is_repair = line.move_id.is_repair if line.move_id else False

    def catch_values_from_create_repair_from_picking(self):
        vals = {
            "partner_id": self.picking_id.partner_id.id,
            "product_id": self.product_id.id,
            "product_qty": self.qty_done,
            "product_uom": self.product_uom_id.id,
            "location_id": self.location_dest_id.id,
            "invoice_method": "after_repair",
            "created_from_move_line_id": self.id,
        }
        if self.lot_id:
            vals["lot_id"] = self.lot_id.id
        if self.picking_id.sale_order_id:
            vals["sale_order_id"] = self.picking_id.sale_order_id.id
        if self.picking_id.origin:
            cond = [("name", "=", self.picking_id.origin)]
            purchase = self.env["purchase.order"].search(cond, limit=1)
            if purchase:
                vals["purchase_order_id"] = purchase.id
        if self.picking_id.sale_order_id:
            sale = self.picking_id.sale_order_id
            vals["partner_invoice_id"] = (
                sale.partner_invoice_id.id
                if sale.partner_invoice_id
                else sale.partner_id.id
            )
            vals["address_id"] = (
                sale.partner_shipping_id.id
                if sale.partner_shipping_id
                else sale.partner_id.id
            )
        return vals
