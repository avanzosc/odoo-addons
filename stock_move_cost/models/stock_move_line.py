# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    price_unit_cost = fields.Float(
        string="Cost Unit Price", digits="Product Price", copy=False
    )
    cost = fields.Float(
        string="Cost",
        digits="Product Price",
        copy=False,
        store=True,
        compute="_compute_cost",
    )

    @api.depends("qty_done", "price_unit_cost")
    def _compute_cost(self):
        for line in self:
            line.cost = line.qty_done * line.price_unit_cost

    @api.onchange("product_id", "product_uom_id")
    def _onchange_product_id(self):
        if self.product_id and self.product_id.standard_price:
            self.price_unit_cost = self.product_id.standard_price
        return super()._onchange_product_id()

    @api.onchange("lot_name", "lot_id")
    def _onchange_serial_number(self):
        result = super()._onchange_serial_number()
        if self.lot_id and self.lot_id.purchase_price:
            self.price_unit_cost = self.lot_id.purchase_price
        return result

    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)
        for line in lines.filtered(lambda x: not x.price_unit_cost):
            line._put_price_unit_cost_in_line()
        return lines

    def write(self, vals):
        result = super().write(vals)
        if "price_unit_cost" not in vals:
            for line in self:
                line._put_price_unit_cost_in_line()
        return result

    def _put_price_unit_cost_in_line(self):
        if self.lot_id and self.lot_id.purchase_price:
            self._onchange_serial_number()
        else:
            if self.price_unit_cost == 0 and self.product_id.standard_price:
                self._onchange_product_id()
