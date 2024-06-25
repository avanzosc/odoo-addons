# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductSupplierInfo(models.Model):
    _inherit = "product.supplierinfo"

    qty_available = fields.Float(
        string="Quantity On Hand",
        digits="Product Unit of Measure",
        compute="_compute_supplierinfo_quantities",
    )
    incoming_qty = fields.Float(
        string="Incoming",
        digits="Product Unit of Measure",
        compute="_compute_supplierinfo_quantities",
    )
    outgoing_qty = fields.Float(
        string="Outgoing",
        digits="Product Unit of Measure",
        compute="_compute_supplierinfo_quantities",
    )
    consumed_last_twelve_months = fields.Float(
        string="Consumed last twelve months",
        digits="Product Unit of Measure",
        compute="_compute_supplierinfo_quantities",
    )
    months_with_stock = fields.Integer(
        string="Months with stock", compute="_compute_supplierinfo_quantities"
    )
    supplier_pending_to_receive = fields.Float(
        string="Pending receipt from supplier",
        compute="_compute_supplier_pending_to_receive",
    )

    def _compute_supplierinfo_quantities(self):
        for supplierinfo in self:
            supplierinfo.qty_available = (
                supplierinfo.product_id.qty_available
                if supplierinfo.product_id
                else supplierinfo.product_tmpl_id.qty_available
            )
            supplierinfo.incoming_qty = (
                supplierinfo.product_id.incoming_qty
                if supplierinfo.product_id
                else supplierinfo.product_tmpl_id.incoming_qty
            )
            supplierinfo.outgoing_qty = (
                supplierinfo.product_id.outgoing_qty
                if supplierinfo.product_id
                else supplierinfo.product_tmpl_id.outgoing_qty
            )
            supplierinfo.consumed_last_twelve_months = (
                supplierinfo.product_id.consumed_last_twelve_months
                if supplierinfo.product_id
                else supplierinfo.product_tmpl_id.consumed_last_twelve_months
            )
            supplierinfo.months_with_stock = (
                supplierinfo.product_id.months_with_stock
                if supplierinfo.product_id
                else supplierinfo.product_tmpl_id.months_with_stock
            )

    def _compute_supplier_pending_to_receive(self):
        stock_move_obj = self.env["stock.move"]
        for supplierinfo in self:
            pending_to_receive = 0
            cond = [
                ("state", "not in", ("done", "draft", "cancel")),
                ("picking_id.partner_id", "=", supplierinfo.name.id),
                ("location_id", "!=", False),
                ("location_id.usage", "=", "supplier"),
                "|",
                ("product_id", "=", supplierinfo.product_id.id),
                ("product_id.product_tmpl_id", "=", supplierinfo.product_tmpl_id.id),
            ]
            stock_moves = stock_move_obj.search(cond)
            if stock_moves:
                pending_to_receive = sum(stock_moves.mapped("product_uom_qty"))
            supplierinfo.supplier_pending_to_receive = pending_to_receive
