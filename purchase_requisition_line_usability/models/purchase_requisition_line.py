# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class PurchaseRequisitionLine(models.Model):
    _inherit = "purchase.requisition.line"

    vendor_id = fields.Many2one(
        string="Supplier",
        comodel_name="res.partner",
        related="requisition_id.vendor_id",
        store=True,
    )
    user_id = fields.Many2one(
        string="Supplier's Representative",
        comodel_name="res.users",
        related="requisition_id.user_id",
        store=True,
    )
    price_unit = fields.Float(digits="Price Unit Decimal Precision")
    shipping_cost = fields.Float(digits="Price Unit Decimal Precision")
    date_end = fields.Date(
        string="Date End", related="requisition_id.date_end", store=True
    )
    ordering_date = fields.Date(
        string="Ordering Date", related="requisition_id.date_start", store=True
    )
    schedule_date = fields.Date(
        string="Schedule Date", related="requisition_id.date_end", store=True
    )
    state = fields.Selection(string="State", related="requisition_id.state", store=True)
    origin = fields.Char(
        string="Origin Document", related="requisition_id.reference", store=True
    )
    dif_qty = fields.Float(string="Pending", compute="_compute_dif_qty")

    @api.depends("requisition_id.purchase_ids.state")
    def _compute_ordered_qty(self):
        res = super()._compute_ordered_qty()
        for line in self:
            total = 0.0
            line_product = line.product_id
            for po in line.requisition_id.purchase_ids.filtered(
                lambda purchase_order: purchase_order.state in ["purchase", "done"]
            ):
                for po_line in po.order_line.filtered(
                    lambda order_line, product=line_product: order_line.product_id
                    == product
                ):
                    if po_line.product_uom != line.product_uom_id:
                        total += po_line.product_uom._compute_quantity(
                            po_line.product_qty, line.product_uom_id
                        )
                    else:
                        total += po_line.product_qty
            line.qty_ordered = total
        return res

    @api.depends("product_qty", "qty_ordered")
    def _compute_dif_qty(self):
        for line in self:
            line.dif_qty = line.product_qty - line.qty_ordered
