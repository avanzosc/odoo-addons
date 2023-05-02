# Copyright 2021 Daniel Campos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import _, models


class StockWarehouseOrderpoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"

    def button_recompute_qty_to_order(self):
        fnames = ["qty_to_order"]
        for fname in fnames:
            self.env.add_to_compute(self._fields[fname], self)
        self.modified(fnames)

    def open_form_view(self):
        self.ensure_one()
        view_ref = self.env["ir.model.data"].get_object_reference(
            "stock", "view_warehouse_orderpoint_form"
        )
        view_id = (view_ref and view_ref[1] or False,)
        return {
            "name": _("Reordering Rule"),
            "domain": [],
            "res_model": "stock.warehouse.orderpoint",
            "res_id": self.id,
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "view_type": "form",
            "view_id": view_id,
            "target": "current",
        }
