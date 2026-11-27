# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    price_unit_cost = fields.Float(
        string="Cost Unit Price",
        digits="Product Price",
        copy=False,
        default=0.0,
    )
    cost = fields.Float(
        digits="Product Price",
        copy=False,
        store=True,
        compute="_compute_cost",
        default=0.0,
    )

    @api.depends("quantity", "price_unit_cost")
    def _compute_cost(self):
        for line in self:
            line.cost = line.quantity * line.price_unit_cost

    def _get_product_price_unit_cost(self):
        self.ensure_one()
        if self.move_id.purchase_line_id:
            return self.move_id.purchase_line_id.price_unit
        return self.product_id.standard_price

    @api.onchange("product_id", "product_uom_id")
    def _onchange_product_id(self):
        if self.product_id:
            self.price_unit_cost = self._get_product_price_unit_cost()
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
        # Do not call onchange methods here: on stored records they write
        # other fields (e.g. description_picking), which triggers write()
        # again and ends in infinite recursion.
        for line in self:
            if line.lot_id and line.lot_id.purchase_price:
                price = line.lot_id.purchase_price
            elif (
                not line.price_unit_cost
                and line.product_id
                and line.product_id.standard_price
            ):
                price = line._get_product_price_unit_cost()
            else:
                continue
            if price != line.price_unit_cost:
                line.price_unit_cost = price
