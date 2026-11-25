# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from datetime import date as date_type

from odoo import fields, models


class StockInventory(models.Model):
    _inherit = "stock.inventory"

    accounting_date = fields.Datetime(default=fields.Datetime.now, copy=False)

    def action_view_inventory_adjustment(self):
        result = super().action_view_inventory_adjustment()
        result.setdefault("context", {})
        is_at_date = bool(
            self.accounting_date and self.accounting_date.date() < date_type.today()
        )
        result["context"].update(
            {
                "inventory_date": self.accounting_date,
                "inventory_is_at_date": is_at_date,
            }
        )
        return result

    def action_state_to_in_progress(self):
        for rec in self.filtered("accounting_date"):
            rec.date = rec.accounting_date
        result = super().action_state_to_in_progress()
        for rec in self.filtered("accounting_date"):
            quants = rec.stock_quant_ids.filtered(
                lambda quant, rec=rec: quant.current_inventory_id == rec
            )
            quants.write({"inventory_date": rec.accounting_date})
            qty_map = rec._get_qty_at_date_batch(quants)
            for quant in quants:
                qty = qty_map.get(quant.id, 0.0)
                quant.write(
                    {
                        "inventory_at_date_qty": qty,
                        "inventory_quantity": qty,
                    }
                )
        return result

    def _get_qty_at_date_batch(self, quants):
        self.ensure_one()
        if not quants:
            return {}
        if self.accounting_date.date() >= date_type.today():
            return {q.id: q.quantity for q in quants}

        product_ids = quants.mapped("product_id").ids
        location_ids = quants.mapped("location_id").ids
        move_line = self.env["stock.move.line"].with_context(active_test=False)

        domain_base = [
            ("product_id", "in", product_ids),
            ("date", "<=", self.accounting_date),
            ("state", "=", "done"),
        ]
        domain_in = domain_base + [("location_dest_id", "in", location_ids)]
        domain_out = domain_base + [("location_id", "in", location_ids)]

        groupby_in = [
            "product_id",
            "location_dest_id",
            "lot_id",
            "owner_id",
            "result_package_id",
        ]
        groupby_out = ["product_id", "location_id", "lot_id", "owner_id", "package_id"]

        in_groups = move_line.read_group(
            domain_in, ["quantity"], groupby_in, lazy=False
        )
        out_groups = move_line.read_group(
            domain_out, ["quantity"], groupby_out, lazy=False
        )

        def _id(val):
            return val[0] if val else False

        in_dict = {}
        for item in in_groups:
            key = (
                _id(item["product_id"]),
                _id(item["location_dest_id"]),
                _id(item["lot_id"]),
                _id(item["owner_id"]),
                _id(item["result_package_id"]),
            )
            in_dict[key] = in_dict.get(key, 0.0) + (item["quantity"] or 0.0)

        out_dict = {}
        for item in out_groups:
            key = (
                _id(item["product_id"]),
                _id(item["location_id"]),
                _id(item["lot_id"]),
                _id(item["owner_id"]),
                _id(item["package_id"]),
            )
            out_dict[key] = out_dict.get(key, 0.0) + (item["quantity"] or 0.0)

        result = {}
        for quant in quants:
            key = (
                quant.product_id.id,
                quant.location_id.id,
                quant.lot_id.id if quant.lot_id else False,
                quant.owner_id.id if quant.owner_id else False,
                quant.package_id.id if quant.package_id else False,
            )
            result[quant.id] = in_dict.get(key, 0.0) - out_dict.get(key, 0.0)
        return result
