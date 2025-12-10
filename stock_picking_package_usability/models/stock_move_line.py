# Copyright 2021 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    shipping_weight = fields.Float(
        string="Shipping Weight",
        compute="_compute_shipping_weight",
        store=True,
    )
    weight_uom_name = fields.Char(
        string="Weight UOM", related="result_package_id.weight_uom_name", store=True
    )

    packaging_id = fields.Many2one(
        "product.packaging",
        string="Package Type",
    )

    dimensions_of_package = fields.Char(
        string="Dimensions of Package",
        related="result_package_id.dimensions_of_package",
        store=True,
        readonly=True,
    )

    @api.depends(
        "qty_done",
        "product_uom_qty",
        "product_id.weight",
        "packaging_id",
        "packaging_id.empty_weight",
    )
    def _compute_shipping_weight(self):
        for line in self:
            weight_line = 0.0
            if line.qty_done > 0:
                weight_line = line.qty_done * (line.product_id.weight or 0.0)
            elif line.product_uom_qty > 0:
                weight_line = line.product_uom_qty * (line.product_id.weight or 0.0)
            if line.result_package_id and line.packaging_id:
                weight_line += line.packaging_id.empty_weight or 0.0
            line.shipping_weight = weight_line

    @api.onchange("result_package_id")
    def _onchange_result_package(self):
        for line in self:
            if line.result_package_id:
                line.packaging_id = line.result_package_id.packaging_id

    @api.model
    def create(self, vals):
        record = super().create(vals)
        record._compute_shipping_weight()
        return record
