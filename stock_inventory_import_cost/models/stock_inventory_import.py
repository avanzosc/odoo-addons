# © 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3 - See https://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class StockInventoryImport(models.Model):
    _inherit = "stock.inventory.import"

    def _get_line_values(self, row_values, datemode=False):
        self.ensure_one()
        values = super()._get_line_values(row_values, datemode=datemode)
        if values and row_values:
            values
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
        states={"done": [("readonly", True)]},
        copy=False,
    )
    inventory_product_amount = fields.Float(
        string="Amount",
        states={"done": [("readonly", True)]},
        copy=False,
    )

    def _action_process(self):
        self.ensure_one()
        result = super()._action_process()
        if self.inventory_product_cost and "inventory_line_id" in result:
            inv_line = self.env["stock.inventory.line"].search(
                [("id", "=", result["inventory_line_id"])], limit=1
            )
            inv_line.write(
                {
                    "cost": self.inventory_product_cost,
                    "amount": self.inventory_product_amount
                    or (self.inventory_product_cost * inv_line.product_qty),
                }
            )
        return result
