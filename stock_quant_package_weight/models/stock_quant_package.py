# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockQuantPackage(models.Model):
    _inherit = "stock.quant.package"

    pack_weight = fields.Float(
        compute="_compute_pack_weight", store=True, readonly=False
    )
    shipping_weight = fields.Float(
        compute="_compute_shipping_weight", store=True, readonly=False
    )
    move_line_ids = fields.One2many(
        string="Move Lines",
        comodel_name="stock.move.line",
        inverse_name="result_package_id",
        copy=False,
    )

    @api.depends(
        "package_type_id",
        "package_type_id.base_weight",
        "product_packaging_id",
        "product_packaging_id.weight",
    )
    def _compute_pack_weight(self):
        for package in self:
            pack_weight = 0
            if package.product_packaging_id and package.product_packaging_id.weight:
                pack_weight = package.product_packaging_id.weight
            else:
                if package.package_type_id and package.package_type_id.base_weight:
                    pack_weight = package.package_type_id.base_weight
            package.pack_weight = pack_weight

    @api.depends("pack_weight", "estimated_pack_weight_kg")
    def _compute_shipping_weight(self):
        for package in self:
            package._compute_estimated_pack_weight_kg()
            package.shipping_weight = (
                package.pack_weight + package.estimated_pack_weight_kg
            )

    @api.depends(
        "quant_ids",
        "move_line_ids",
        "move_line_ids.result_package_id",
        "move_line_ids.weight",
    )
    @api.depends_context("picking_id")
    def _compute_estimated_pack_weight_kg(self):
        result = super()._compute_estimated_pack_weight_kg()
        for package in self:
            estimated_pack_weight_kg = 0
            if package.move_line_ids:
                move_line_ids = package.move_line_ids.filtered(
                    lambda x: x.state != "cancel"
                )
                if move_line_ids:
                    estimated_pack_weight_kg = sum(move_line_ids.mapped("weight"))
            package.estimated_pack_weight_kg = estimated_pack_weight_kg
        return result
