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
    shipping_weight = fields.Float(
        string="Shipping Weight",
        compute="_compute_shipping_weight",
        store=True,
    )
    weight_uom_name = fields.Char(
        string="Weight UOM", related="result_package_id.weight_uom_name", store=True
    )

    @api.depends(
        "qty_done",
        "product_uom_qty",
        "product_id.weight",
        "result_package_id.shipping_weight",
    )
    def _compute_shipping_weight(self):
        for line in self:
            weight_line = 0.0
            if line.qty_done > 0:
                weight_line = line.qty_done * (line.product_id.weight or 0.0)
            elif line.product_uom_qty > 0:
                weight_line = line.product_uom_qty * (line.product_id.weight or 0.0)
            if line.result_package_id:
                weight_line += line.result_package_id.shipping_weight or 0.0
            line.shipping_weight = weight_line

    @api.onchange("result_package_id", "packaging_id", "qty_done", "product_uom_qty")
    def _onchange_package_or_qty(self):
        self._compute_shipping_weight()
        if self.result_package_id:
            for line in self.result_package_id.move_line_ids:
                line._compute_shipping_weight()

    @api.model
    def create(self, vals):
        record = super().create(vals)
        record._compute_shipping_weight()
        return record

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
