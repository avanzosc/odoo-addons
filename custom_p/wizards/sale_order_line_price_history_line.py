# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class SaleOrderLinePriceHistoryline(models.TransientModel):
    _inherit = "sale.order.line.price.history.line"

    commitment_date = fields.Datetime(
        string="Commitment Date",
        related="sale_order_line_id.commitment_date",
    )
    lot_id = fields.Many2one(
        string="Lot/Serial Number",
        comodel_name="stock.production.lot",
        related="sale_order_line_id.lot_id",
    )
