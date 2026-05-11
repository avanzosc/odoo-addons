# Copyright 2021 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    packaging_id = fields.Many2one(
        string="Packaging",
        comodel_name="product.packaging",
    )
    line_weight = fields.Float(
        compute="_compute_weight_line",
        store=True,
    )
    manual_pack_weight = fields.Float(string="Pack Weight")
    shipping_weight = fields.Float(
        string="Shipping Weight",
        related="result_package_id.shipping_weight",
        readonly=False,
        store=True,
    )
    weight_uom_name = fields.Char(
        string="Weight UOM", related="result_package_id.weight_uom_name", store=True
    )

    @api.depends("quantity", "move_id.product_uom_qty", "product_id.weight")
    def _compute_weight_line(self):
        for line in self:
            qty = (
                line.quantity
                if line.quantity > 0
                else (line.move_id.product_uom_qty or 0.0)
            )
            line.line_weight = qty * (line.product_id.weight or 0.0)

    @api.onchange("manual_pack_weight")
    def _onchange_manual_pack_weight(self):
        for line in self:
            package = line.result_package_id
            if package:
                package.pack_weight = line.manual_pack_weight
                for other_line in package.move_line_ids:
                    if other_line != line:
                        other_line.manual_pack_weight = line.manual_pack_weight

    def write(self, values):
        result = super().write(values)
        if "result_package_id" in values:
            for line in self:
                if not line.result_package_id:
                    continue
                package = line.result_package_id
                package.picking_id = line.picking_id
                if package.product_packaging_id:
                    line.with_context(
                        skip_package_sync=True
                    ).packaging_id = package.product_packaging_id
                elif line.packaging_id:
                    package.with_context(
                        _auto_assign_packaging=True
                    ).product_packaging_id = line.packaging_id
        if "packaging_id" in values and not self.env.context.get("skip_package_sync"):
            for line in self:
                if (
                    line.result_package_id
                    and not line.result_package_id.product_packaging_id
                ):
                    line.result_package_id.with_context(
                        _auto_assign_packaging=True
                    ).product_packaging_id = line.packaging_id
        return result

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if "move_id" in vals and "packaging_id" not in vals:
                move = self.env["stock.move"].browse(vals.get("move_id"))
                if move and move.product_packaging_id:
                    vals["packaging_id"] = move.product_packaging_id.id
        return super().create(vals_list)
