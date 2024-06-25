# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, fields, models


class SacaLine(models.Model):
    _inherit = "saca.line"

    sale_order_id = fields.Many2one(
        string="Sale Order",
        comodel_name="sale.order",
        related="sale_order_line_ids.order_id",
        store=True,
    )
    sale_order_line_ids = fields.One2many(
        string="Sale Orden Line",
        comodel_name="sale.order.line",
        inverse_name="saca_line_id",
    )
    stock_move_ids = fields.One2many(
        string="Stock Move", comodel_name="stock.move", inverse_name="saca_line_id"
    )
    move_line_ids = fields.One2many(
        string="Move Line", comodel_name="stock.move.line", inverse_name="saca_line_id"
    )
    picking_ids = fields.One2many(
        string="Pickings", comodel_name="stock.picking", compute="_compute_picking_ids"
    )
    sale_ids = fields.One2many(
        string="Sale Order", comodel_name="sale.order", compute="_compute_sale_ids"
    )
    count_picking = fields.Integer(
        string="Count Pickings", compute="_compute_count_picking"
    )
    count_sale = fields.Integer(string="Count Salses", compute="_compute_count_sale")

    def _compute_count_sale(self):
        for line in self:
            self.count_sale = len(line.sale_ids)

    def _compute_count_picking(self):
        for line in self:
            self.count_picking = len(line.picking_ids)

    def _compute_sale_ids(self):
        for line in self:
            sales = []
            if line.sale_order_id:
                sales.append(line.sale_order_id.id)
            line.sale_ids = [(6, 0, sales)]

    def _compute_picking_ids(self):
        for line in self:
            picking = []
            for move in line.stock_move_ids:
                if move.picking_id.id not in picking:
                    picking.append(move.picking_id.id)
            line.picking_ids = [(6, 0, picking)]

    def action_view_picking_ids(self):
        context = self.env.context.copy()
        return {
            "name": _("Pickings"),
            "view_mode": "tree,form",
            "res_model": "stock.picking",
            "domain": [("id", "in", self.picking_ids.ids)],
            "type": "ir.actions.act_window",
            "context": context,
        }

    def action_view_sale_ids(self):
        context = self.env.context.copy()
        return {
            "name": _("Sale Order"),
            "view_mode": "tree,form",
            "res_model": "sale.order",
            "domain": [("id", "in", self.sale_ids.ids)],
            "type": "ir.actions.act_window",
            "context": context,
        }
