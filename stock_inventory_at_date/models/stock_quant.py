# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from datetime import date as date_type

from odoo import api, fields, models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    inventory_at_date_qty = fields.Float(
        string="Qty at Inventory Date",
        digits="Product Unit of Measure",
        store=True,
        readonly=True,
    )

    @api.depends(
        "inventory_quantity",
        "quantity",
        "inventory_at_date_qty",
        "current_inventory_id.accounting_date",
    )
    def _compute_inventory_diff_quantity(self):
        for quant in self:
            inventory = quant.current_inventory_id
            if (
                inventory
                and getattr(inventory, "accounting_date", False)
                and inventory.accounting_date.date() < date_type.today()
            ):
                quant.inventory_diff_quantity = (
                    quant.inventory_quantity - quant.inventory_at_date_qty
                )
            else:
                quant.inventory_diff_quantity = (
                    quant.inventory_quantity - quant.quantity
                )

    @api.depends(
        "inventory_quantity",
        "quantity",
        "product_id",
        "inventory_at_date_qty",
        "current_inventory_id.accounting_date",
    )
    def _compute_is_outdated(self):
        res = super()._compute_is_outdated()
        for quant in self:
            inventory = quant.current_inventory_id
            if (
                inventory
                and getattr(inventory, "accounting_date", False)
                and inventory.accounting_date.date() < date_type.today()
            ):
                quant.is_outdated = False
        return res

    def _apply_inventory(self):
        inventory_dates = {}
        for quant in self.filtered("current_inventory_id"):
            inventory = quant.current_inventory_id
            if (
                getattr(inventory, "accounting_date", False)
                and inventory.accounting_date.date() < date_type.today()
            ):
                inventory_dates[inventory.id] = inventory.accounting_date

        res = super()._apply_inventory()

        for inv_id, accounting_date in inventory_dates.items():
            inventory = self.env["stock.inventory"].browse(inv_id)
            move_lines = inventory.stock_move_ids
            moves = move_lines.mapped("move_id")
            move_lines.write({"date": accounting_date})
            moves.write({"date": accounting_date})

        return res
