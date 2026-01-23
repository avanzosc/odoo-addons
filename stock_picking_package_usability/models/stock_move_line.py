# Copyright 2021 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    packaging_id = fields.Many2one(
        string="Package Type",
        comodel_name="product.packaging",
        related="result_package_id.packaging_id",
        store=True,
        readonly=False,
    )

    line_weight = fields.Float(
        string="weight line",
        compute="_compute_weight_line",
        store=True,
    )

    weight_uom_name = fields.Char(
        string="Weight UOM", related="result_package_id.weight_uom_name", store=True
    )

    manual_pack_weight = fields.Float(
        string="Pack Weight",
    )

    @api.onchange("manual_pack_weight")
    def onchange_manual_pack_weight(self):
        for line in self:
            package = line.result_package_id
            if package:
                package.pack_weight = line.manual_pack_weight
                for other_line in package.move_line_ids:
                    if other_line != line:
                        other_line.manual_pack_weight = line.manual_pack_weight

    @api.onchange("packaging_id")
    def _onchange_packaging_id(self):
        for line in self:
            package = line.result_package_id
            if package and line.packaging_id:
                package.length_uom_id = line.packaging_id.length_uom_id

    def write(self, values):
        result = super().write(values)
        if "result_package_id" in values:
            for line in self:
                line.result_package_id.picking_id = line.picking_id.id
                line.result_package_id.height = line.packaging_id.height
                line.result_package_id.width = line.packaging_id.width
                line.result_package_id.pack_length = line.packaging_id.packaging_length
                line.result_package_id.max_weight = line.packaging_id.max_weight
        if "packaging_id" in values:
            for line in self:
                if not line.result_package_id.height:
                    line.result_package_id.height = line.packaging_id.height
                if not line.result_package_id.width:
                    line.result_package_id.width = line.packaging_id.width
                if not line.result_package_id.pack_length:
                    line.result_package_id.pack_length = (
                        line.packaging_id.packaging_length
                    )
                if not line.result_package_id.max_weight:
                    line.result_package_id.max_weight = line.packaging_id.max_weight
        return result

    @api.depends("qty_done", "product_uom_qty", "product_id.weight")
    def _compute_weight_line(self):
        for line in self:
            qty = (
                line.qty_done
                if line.qty_done > 0
                else (line.product_uom_qty if line.product_uom_qty > 0 else 0.0)
            )
            line.line_weight = qty * (line.product_id.weight or 0.0)
