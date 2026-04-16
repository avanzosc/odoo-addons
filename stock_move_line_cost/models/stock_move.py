# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    standard_price = fields.Float(string="Cost", digits="Product Price")
    amount = fields.Float(compute="_compute_amount", store=True, digits="Product Price")

    @api.depends("standard_price", "quantity")
    def _compute_amount(self):
        for move in self:
            move.amount = move.standard_price * move.quantity

    def _get_standard_price_from_source(self):
        self.ensure_one()
        if self.sale_line_id:
            return self.sale_line_id.price_unit
        if self.purchase_line_id:
            return self.purchase_line_id.price_unit
        if self.product_id:
            return self.product_id.standard_price
        return 0.0

    def _set_standard_price_from_source(self, force=False):
        for move in self:
            if force or not move.standard_price:
                move.standard_price = move._get_standard_price_from_source()

    @api.model_create_multi
    def create(self, vals_list):
        moves = super().create(vals_list)
        for move, vals in zip(moves, vals_list, strict=False):
            if "standard_price" not in vals:
                move._set_standard_price_from_source()
        return moves

    def write(self, vals):
        update_from_source = "standard_price" not in vals and any(
            key in vals for key in ("sale_line_id", "purchase_line_id", "product_id")
        )
        result = super().write(vals)
        if update_from_source:
            self._set_standard_price_from_source(force=True)
        return result

    @api.onchange("sale_line_id", "purchase_line_id", "product_id")
    def _onchange_standard_price_source(self):
        self._set_standard_price_from_source(force=True)
