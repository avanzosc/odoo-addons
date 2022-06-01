# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, fields, models


class Saca(models.Model):
    _inherit = "saca"

    sale_order_line_ids = fields.One2many(
        string="Sale Order Lines",
        comodel_name="sale.order.line",
        inverse_name="saca_id")
    sale_line_count = fields.Integer(
        string="# Sale Order Lines",
        compute="_compute_sale_line_count")
    sale_order_ids = fields.One2many(
        string="Sale Order",
        comodel_name="sale.order",
        inverse_name="saca_id")
    sale_count = fields.Integer(
        string="# Sale Orders",
        compute="_compute_sale_count")
    stock_move_ids = fields.One2many(
        string="Stock Move",
        comodel_name="stock.move",
        inverse_name="saca_id")
    stock_move_count = fields.Integer(
        string="# Stock Moves",
        compute="_compute_stock_move_count")
    move_line_ids = fields.One2many(
        string="Move Line",
        comodel_name="stock.move.line",
        inverse_name="saca_id")
    move_line_count = fields.Integer(
        string="# Move Lines",
        compute="_compute_move_lines_count")

    def _compute_sale_line_count(self):
        for saca in self:
            saca.sale_line_count = len(saca.sale_order_line_ids)

    def _compute_sale_count(self):
        for saca in self:
            saca.sale_count = len(saca.sale_order_ids)

    def _compute_stock_move_count(self):
        for saca in self:
            saca.stock_move_count = len(saca.stock_move_ids)

    def _compute_move_lines_count(self):
        for saca in self:
            saca.move_line_count = len(saca.move_line_ids)

    def action_view_sale_order_line(self):
        context = self.env.context.copy()
        context.update({"default_saca_id": self.id})
        return {
            "name": _("Sale Order Lines"),
            "view_mode": "tree,form",
            "res_model": "sale.order.line",
            "domain": [("id", "in", self.sale_order_line_ids.ids)],
            "type": "ir.actions.act_window",
            "context": context
        }

    def action_view_sale_order(self):
        context = self.env.context.copy()
        context.update({"default_saca_id": self.id})
        return {
            "name": _("Sale Orders"),
            "view_mode": "tree,form",
            "res_model": "sale.order",
            "domain": [("id", "in", self.sale_order_ids.ids)],
            "type": "ir.actions.act_window",
            "context": context
        }

    def action_view_stock_move(self):
        context = self.env.context.copy()
        context.update({"default_saca_id": self.id})
        return {
            "name": _("Stock Moves"),
            "view_mode": "tree,form",
            "res_model": "stock.move",
            "domain": [("id", "in", self.stock_move_ids.ids)],
            "type": "ir.actions.act_window",
            "context": context
        }

    def action_view_move_line(self):
        context = self.env.context.copy()
        context.update({"default_saca_id": self.id})
        return {
            "name": _("Move Lines"),
            "view_mode": "tree,form",
            "res_model": "stock.move.line",
            "domain": [("id", "in", self.move_line_ids.ids)],
            "type": "ir.actions.act_window",
            "context": context
        }
