# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class SacaLine(models.Model):
    _inherit = "saca.line"

    sale_order_id = fields.Many2one(
        string="Sale Order",
        comodel_name="sale.order",
        related="sale_order_line_ids.order_id",
        store=True)
    sale_order_line_ids = fields.One2many(
        string="Sale Orden Line",
        comodel_name="sale.order.line",
        inverse_name="saca_line_id",
        copy=False)
    stock_move_ids = fields.One2many(
        string="Stock Move",
        comodel_name="stock.move",
        inverse_name="saca_line_id",
        copy=False)
    move_line_ids = fields.One2many(
        string="Move Line",
        comodel_name="stock.move.line",
        inverse_name="saca_line_id",
        copy=False)
