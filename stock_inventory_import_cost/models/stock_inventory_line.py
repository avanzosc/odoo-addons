# © 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3 - See https://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class StockInventoryLine(models.Model):
    _inherit = "stock.inventory.line"

    cost = fields.Float(
        string="Cost",
    )
    amount = fields.Float(
        string="Amount",
    )

    @api.onchange("product_id")
    def onchange_cost(self):
        if self.product_id and self.product_id.standard_price:
            self.cost = self.product_id.standard_price

    @api.onchange("cost", "difference_qty")
    def onchange_amount(self):
        self.amount = self.cost * abs(self.difference_qty)

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        for line in res:
            line.onchange_cost()
            line.onchange_amount()
        return res

    def _get_move_values(self, qty, location_id, location_dest_id, out):
        values = super()._get_move_values(qty, location_id, location_dest_id, out)
        values.update({"standard_price": self.cost, "amount": self.amount})
        values["move_line_ids"][0][2].update(
            {"standard_price": self.cost, "amount": self.amount}
        )
        return values
