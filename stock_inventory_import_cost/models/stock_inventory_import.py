# © 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3 - See https://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class StockInventoryImport(models.Model):
    _inherit = "stock.inventory.import"

    def _get_line_values(self, row_values, datemode=False):
        self.ensure_one()
        values = super()._get_line_values(row_values, datemode=datemode)
        if values and row_values:
            inventory_product_cost = row_values.get("Precio", "")
            inventory_product_amount = row_values.get("Importe", "")
            values.update(
                {
                    "inventory_product_cost": inventory_product_cost,
                    "inventory_product_amount": inventory_product_amount,
                }
            )
        return values


class StockInventoryImportLine(models.Model):
    _inherit = "stock.inventory.import.line"

    inventory_product_cost = fields.Float(
        string="Cost",
        copy=False,
    )
    inventory_product_amount = fields.Float(
        string="Amount",
        copy=False,
    )

    def _action_process(self):
        self.ensure_one()
        result = super()._action_process()
        if not self.inventory_product_cost:
            return result
        quant_id = result.get("quant_id") or self.quant_id.id
        if not quant_id:
            return result
        quant = self.env["stock.quant"].browse(quant_id).exists()
        if not quant:
            return result
        inventory_location = quant.product_id.with_company(
            quant.company_id
        ).property_stock_inventory
        line = self.env["stock.move.line"].search(
            [
                ("is_inventory", "=", True),
                ("state", "=", "done"),
                ("product_id", "=", quant.product_id.id),
                ("lot_id", "=", quant.lot_id.id),
                ("owner_id", "=", quant.owner_id.id),
                "|",
                ("package_id", "=", quant.package_id.id),
                ("result_package_id", "=", quant.package_id.id),
                "|",
                "&",
                ("location_id", "=", quant.location_id.id),
                ("location_dest_id", "=", inventory_location.id),
                "&",
                ("location_id", "=", inventory_location.id),
                ("location_dest_id", "=", quant.location_id.id),
            ],
            order="id desc",
            limit=1,
        )
        if line:
            line.standard_price = self.inventory_product_cost
        return result
