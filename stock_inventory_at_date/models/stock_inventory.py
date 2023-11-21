# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models
from datetime import date


class StockInventory(models.Model):
    _inherit = "stock.inventory"

    accounting_date = fields.Date(
        string="Date",
        default=fields.Date.today())

    def action_open_inventory_lines(self):
        result = super(StockInventory, self).action_open_inventory_lines()
        result["context"].update({
            "inventory_date": self.accounting_date})
        return result

    def _get_inventory_lines_values(self):
        today = date.today()
        vals = super(StockInventory, self)._get_inventory_lines_values()
        if today != self.accounting_date:
            for group in vals:
                product = self.env["product.product"].browse(
                    group["product_id"])
                location = group["location_id"] or False
                lot = group[
                    "prod_lot_id"] if "prod_lot_id" in group else False
                owner = group[
                    "partner_id"] if "partner_id" in group else False
                package = group[
                    "package_id"] if "package_id" in group else False
                qty = product.with_context(
                    location=location,
                    to_date=self.accounting_date,
                    lot_id=lot,
                    owner_id=owner,
                    package_id=package).qty_available
                if group[
                    "product_qty"] != qty and (
                        self.prefill_counted_quantity == "counted"):
                    group["product_qty"] = qty
        return vals

    def action_validate(self):
        result = super(StockInventory, self).action_validate()
        if self.accounting_date:
            for move in self.move_ids:
                move.date = self.accounting_date
                for line in move.move_line_ids:
                    line.date = self.accounting_date
        return result
