# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockLot(models.Model):
    _inherit = "stock.lot"

    pricing_method = fields.Selection(
        related="product_id.pricing_method",
        store=True,
    )
    product_length = fields.Float(
        string="Length",
        digits="Product Dimension",
        related="product_id.product_length",
        store=True,
    )
    product_height = fields.Float(
        string="Height",
        digits="Product Dimension",
        related="product_id.product_height",
        store=True,
    )
    product_width = fields.Float(
        string="Width",
        digits="Product Dimension",
        related="product_id.product_width",
        store=True,
    )
    product_dimensional_uom_id = fields.Many2one(
        comodel_name="uom.uom",
        string="Dimensional UoM",
        related="product_id.dimensional_uom_id",
        store=True,
    )
    product_volume = fields.Float(
        string="Volume",
        digits="Volume",
        related="product_id.volume",
        store=True,
    )
    product_volume_uom_name = fields.Char(
        string="Volume UoM",
        related="product_id.volume_uom_name",
    )
    product_weight = fields.Float(
        string="Weight",
        digits="Product Dimension Weight",
        related="product_id.weight",
        store=True,
    )
    product_weight_uom_name = fields.Char(
        string="Weight UoM",
        related="product_id.weight_uom_name",
    )
