# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    price_unit_cost = fields.Float(
        string="Cost Unit Price", digits="Product Price", copy=False
    )
    cost = fields.Float(
        string="Cost", digits="Product Price", copy=False
    )

    @api.model_create_multi
    def create(self, vals_list):
        lines = super(StockMoveLine, self).create(vals_list)
        lines._put_price_unit_cost_in_move_lines()
        return lines

    def write(self, vals):
        if "lot_id" in vals and vals.get("lot_id", False):
            if isinstance(vals.get("lot_id"), int):
                lot = self.env["stock.lot"].browse(vals.get("lot_id"))
            else:
                lot = vals.get("lot_id")
            price_unit = self.product_id.standard_price
            if lot.purchase_price:
                price_unit = lot.purchase_price
            vals["price_unit_cost"] = price_unit
        result = super(StockMoveLine, self).write(vals)
        return result

    def _action_done(self):
        result = super(StockMoveLine, self)._action_done()
        for line in self:
            cost = line.price_unit_cost * line.qty_done
            if line.cost != cost:
                line.cost = cost
        return result

    def _put_price_unit_cost_in_move_lines(self):
        for line in self:
            price_unit = line.product_id.standard_price
            if line.lot_id and line.lot_id.purchase_price:
                price_unit = line.lot_id.purchase_price
            vals = {}
            if line.price_unit_cost != price_unit:
                vals["price_unit_cost"] = price_unit
            if line.state == "done":
                cost = price_unit * line.qty_done
                if line.cost != cost:
                    vals["cost"] = cost
            if vals:
                line.write(vals)
