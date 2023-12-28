# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models
from datetime import date


class StockInventoryLine(models.Model):
    _inherit = "stock.inventory.line"

    @api.model_create_multi
    def create(self, vals_list):
        for group in vals_list:
            if "inventory_id" in group:
                inventory = self.env["stock.inventory"].browse(group[
                    "inventory_id"])
                today = date.today()
                if inventory and (
                    inventory.accounting_date) and (
                        inventory.accounting_date != today):
                    product = self.env["product.product"].browse(
                        group["product_id"])
                    location = group["location_id"] or False
                    lot = group[
                        "prod_lot_id"] if "prod_lot_id" in group and group[
                        "prod_lot_id"] else False
                    owner = group[
                        "partner_id"] if "partner_id" in group else False
                    package = group[
                        "package_id"] if "package_id" in group else False
                    qty = product.with_context(
                        location=location,
                        to_date=inventory.accounting_date,
                        lot_id=lot,
                        owner_id=owner,
                        package_id=package).qty_available
                    group["theoretical_qty"] = qty
                    group["inventory_date"] = inventory.accounting_date
        res = super(StockInventoryLine, self).create(vals_list)
        return res

    def _get_move_values(self, qty, location_id, location_dest_id, out):
        values = super(StockInventoryLine, self)._get_move_values(
            qty, location_id, location_dest_id, out)
        inventory = self.env["stock.inventory"].browse(values["inventory_id"])
        values["date"] = inventory.accounting_date
        values["move_line_ids"][0][2]["date"] = inventory.accounting_date
        return values
