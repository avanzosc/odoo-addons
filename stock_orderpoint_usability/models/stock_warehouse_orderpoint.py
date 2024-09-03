# Copyright 2021 Daniel Campos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import _, fields, models


class StockWarehouseOrderpoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"

    qty_available = fields.Float(
        string="Quantity On Hand",
        digits="Product Unit of Measure",
        related="product_id.qty_available",
    )
    incoming_qty = fields.Float(
        string="Incoming",
        digits="Product Unit of Measure",
        related="product_id.incoming_qty",
    )
    outgoing_qty = fields.Float(
        string="Outgoing",
        digits="Product Unit of Measure",
        related="product_id.outgoing_qty",
    )
    consumed_last_twelve_months = fields.Float(
        string="Consumed last twelve months",
        digits="Product Unit of Measure",
        related="product_id.consumed_last_twelve_months",
    )
    months_with_stock = fields.Integer(
        string="Months with stock", related="product_id.months_with_stock"
    )
    supplier_pending_to_receive = fields.Float(
        string="Pending receipt from supplier",
        related="supplier_id.supplier_pending_to_receive",
    )

    def button_recompute_qty_to_order(self):
        fnames = ["qty_to_order"]
        for fname in fnames:
            self.env.add_to_compute(self._fields[fname], self)
        self.modified(fnames)

    def open_form_view(self):
        self.ensure_one()
        view_ref = self.env["ir.model.data"]._xmlid_to_res_id(
            "stock.view_warehouse_orderpoint_form"
        )
        # view_id = (view_ref and view_ref[1] or False,)
        return {
            "name": _("Reordering Rule"),
            "domain": [],
            "res_model": "stock.warehouse.orderpoint",
            "res_id": self.id,
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "view_type": "form",
            "view_id": view_ref,
            "target": "current",
        }
