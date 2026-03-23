# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    standard_price = fields.Float(string="Cost", digits="Product Price")
    amount = fields.Float(compute="_compute_amount", store=True, digits="Product Price")

    @api.depends("standard_price", "quantity")
    def _compute_amount(self):
        for line in self:
            line.amount = line.standard_price * line.quantity

    def _get_standard_price_from_source(self):
        self.ensure_one()
        if self.move_id and self.move_id.sale_line_id:
            return self.move_id.sale_line_id.price_unit
        if self.move_id and self.move_id.purchase_line_id:
            return self.move_id.purchase_line_id.price_unit
        if self.product_id:
            return self.product_id.standard_price
        return 0.0

    def _set_standard_price_from_source(self, force=False):
        for line in self:
            if force or not line.standard_price:
                line.standard_price = line._get_standard_price_from_source()

    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)
        for line, vals in zip(lines, vals_list, strict=False):
            if "standard_price" not in vals:
                line._set_standard_price_from_source()
        return lines

    def write(self, vals):
        update_from_source = "standard_price" not in vals and any(
            key in vals for key in ("move_id", "product_id")
        )
        result = super().write(vals)
        if update_from_source:
            self._set_standard_price_from_source(force=True)
        return result

    @api.onchange("move_id", "product_id", "product_uom_id")
    def _onchange_product_id(self):
        result = super()._onchange_product_id()
        self._set_standard_price_from_source(force=True)
        return result

    @api.onchange("lot_id")
    def _onchange_lot_id(self):
        if not self.standard_price:
            self._set_standard_price_from_source()
