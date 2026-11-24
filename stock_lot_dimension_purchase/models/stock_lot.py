# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models

from odoo.addons.stock_lot_dimension.models.product_category import (
    PRICING_METHOD_SELECTION,
)


class StockLot(models.Model):
    """Purchase dimensional information, copied from the purchase order line
    when the lot is created on reception. Informative only."""

    _inherit = "stock.lot"

    purchase_pricing_method = fields.Selection(
        selection=PRICING_METHOD_SELECTION,
        readonly=True,
    )
    theoretical_length = fields.Float(
        string="Purchase Theoretical Length",
        digits="Product Dimension",
        readonly=True,
    )
    theoretical_weight = fields.Float(
        string="Purchase Theoretical Weight",
        digits="Product Dimension Weight",
        readonly=True,
    )
    purchase_length = fields.Float(
        digits="Product Dimension",
        readonly=True,
    )
    purchase_length_uom_id = fields.Many2one(
        comodel_name="uom.uom",
        string="Purchase Length UoM",
        readonly=True,
    )
    purchase_weight = fields.Float(
        digits="Product Dimension Weight",
        readonly=True,
    )
    purchase_weight_uom_id = fields.Many2one(
        comodel_name="uom.uom",
        string="Purchase Weight UoM",
        readonly=True,
    )
