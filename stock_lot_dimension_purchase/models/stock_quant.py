# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockQuant(models.Model):
    """Purchase dimensional information of the quant lot."""

    _inherit = "stock.quant"

    purchase_pricing_method = fields.Selection(
        related="lot_id.purchase_pricing_method",
        store=True,
    )
    theoretical_length = fields.Float(
        related="lot_id.theoretical_length",
        store=True,
    )
    theoretical_weight = fields.Float(
        related="lot_id.theoretical_weight",
        store=True,
    )
    purchase_length = fields.Float(
        related="lot_id.purchase_length",
        store=True,
    )
    purchase_length_uom_id = fields.Many2one(
        related="lot_id.purchase_length_uom_id",
        store=True,
    )
    purchase_weight = fields.Float(
        related="lot_id.purchase_weight",
        store=True,
    )
    purchase_weight_uom_id = fields.Many2one(
        related="lot_id.purchase_weight_uom_id",
        store=True,
    )
