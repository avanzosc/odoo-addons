# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from datetime import date

from odoo import api, models


class StockInventoryLine(models.Model):
    _inherit = "stock.inventory.line"

    @api.model_create_multi
    def create(self, vals_list):
        for group in vals_list:
            if "inventory_id" in group:
                inventory = self.env["stock.inventory"].browse(group["inventory_id"])
                today = date.today()
                if (
                    inventory
                    and (inventory.accounting_date)
                    and (inventory.accounting_date != today)
                ):
                    product = self.env["product.product"].browse(group["product_id"])
                    location = group["location_id"] or False
                    lot = (
                        group["prod_lot_id"]
                        if "prod_lot_id" in group and group["prod_lot_id"]
                        else False
                    )
                    owner = group["partner_id"] if "partner_id" in group else False
                    package = group["package_id"] if "package_id" in group else False
                    domain_move_in = [
                        ("product_id", "=", product.id),
                        ("location_dest_id", "=", location),
                        ("date", "<=", inventory.accounting_date),
                        ("state", "=", "done"),
                    ]
                    domain_move_out = [
                        ("product_id", "=", product.id),
                        ("location_id", "=", location),
                        ("date", "<=", inventory.accounting_date),
                        ("state", "=", "done"),
                    ]
                    if lot:
                        domain_move_in += [("lot_id", "=", lot)]
                        domain_move_out += [("lot_id", "=", lot)]
                    if owner:
                        domain_move_in += [("owner_id", "=", owner)]
                        domain_move_out += [("owner_id", "=", owner)]
                    if package:
                        domain_move_in += [("package_id", "=", package)]
                        domain_move_out += [("package_id", "=", package)]
                    MoveLine = self.env["stock.move.line"].with_context(
                        active_test=False
                    )
                    moves_in = {
                        item["product_id"][0]: item["qty_done"]
                        for item in (
                            MoveLine.read_group(
                                domain_move_in,
                                ["product_id", "qty_done"],
                                ["product_id"],
                                orderby="id",
                            )
                        )
                    }
                    if moves_in and moves_in[product.id]:
                        qty_in = moves_in[product.id]
                    else:
                        qty_in = 0
                    moves_out = {
                        item["product_id"][0]: item["qty_done"]
                        for item in (
                            MoveLine.read_group(
                                domain_move_out,
                                ["product_id", "qty_done"],
                                ["product_id"],
                                orderby="id",
                            )
                        )
                    }
                    if moves_out and moves_out[product.id]:
                        qty_out = moves_out[product.id]
                    else:
                        qty_out = 0
                    qty = qty_in - qty_out
                    group["theoretical_qty"] = qty
                    group["inventory_date"] = inventory.accounting_date
                    if (
                        "product_qty" in group
                        and group["product_qty"] != (group["theoretical_qty"])
                        and (inventory.prefill_counted_quantity == "counted")
                    ):
                        group["product_qty"] = group["theoretical_qty"]
        res = super().create(vals_list)
        return res

    def _get_move_values(self, qty, location_id, location_dest_id, out):
        values = super()._get_move_values(qty, location_id, location_dest_id, out)
        inventory = self.env["stock.inventory"].browse(values["inventory_id"])
        values["date"] = inventory.accounting_date
        values["move_line_ids"][0][2]["date"] = inventory.accounting_date
        return values
