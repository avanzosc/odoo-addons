# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class SacaLine(models.Model):
    _inherit = "saca.line"

    sale_order_id = fields.Many2one(
        string="Sale Order",
        comodel_name="sale.order",
        related="sale_order_line_id.order_id",
        store=True)
    sale_order_line_id = fields.Many2one(
        string="Sale Orden Line",
        comodel_name="sale.order.line",
        compute="_compute_sale_order_line",
        store=True)
    stock_move_ids = fields.One2many(
        string="Stock Move",
        comodel_name="stock.move",
        inverse_name="saca_line_id")
    move_line_ids = fields.One2many(
        string="Move Line",
        comodel_name="stock.move.line",
        inverse_name="saca_line_id")

    @api.depends("saca_id.sale_order_line_ids")
    def _compute_sale_order_line(self):
        for line in self:
            cond = [("saca_line_id", "=", line.id)]
            sale_line = self.saca_id.sale_order_line_ids.search(cond, limit=1)
            if sale_line:
                line.sale_order_line_id = sale_line.id
            else:
                line.sale_order_line_id = False
