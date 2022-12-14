# Copyright 2021 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    packaging_id = fields.Many2one(
        string='Package Type',
        comodel_name='product.packaging',
        related='result_package_id.packaging_id',
        store=True,
        readonly=False)
    shipping_weight = fields.Float(
        string='Shipping Weight',
        related='result_package_id.shipping_weight',
        readonly=False)
    weight_uom_name = fields.Char(
        string='Weight UOM',
        related='result_package_id.weight_uom_name',
        store=True)

    def write(self, values):
        result = super(StockMoveLine, self).write(values)
        if "result_package_id" in values:
            for line in self:
                line.result_package_id.picking_id = line.picking_id.id
                line.result_package_id.height = line.packaging_id.height
                line.result_package_id.width = line.packaging_id.width
                line.result_package_id.pack_length = (
                    line.packaging_id.packaging_length)
                line.result_package_id.max_weight = (
                    line.packaging_id.max_weight)
        if "packaging_id" in values:
            for line in self:
                line.result_package_id.height = line.packaging_id.height
                line.result_package_id.width = line.packaging_id.width
                line.result_package_id.pack_length = (
                    line.packaging_id.packaging_length)
                line.result_package_id.max_weight = (
                    line.packaging_id.max_weight)
        return result
