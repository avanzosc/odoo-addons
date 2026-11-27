# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    purchase_length = fields.Float(
        string="Purchase Length",
        digits="Product Dimension",
        related="purchase_line_id.product_length",
    )
    purchase_length_uom_id = fields.Many2one(
        comodel_name="uom.uom",
        string="Purchase Length UoM",
        related="purchase_line_id.purchase_length_uom_id",
    )
