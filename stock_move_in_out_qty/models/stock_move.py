# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    origin_qty = fields.Float(
        string="Origin Qty",
        compute="_compute_origin_qty",
        store=True)
    dest_qty = fields.Float(
        string="Dest Qty",
        compute="_compute_dest_qty",
        store=True)
    origin_amount = fields.Float(
        string="Origin Amount",
        compute="_compute_origin_amount",
        store=True)
    dest_amount = fields.Float(
        string="Dest Amount",
        compute="_compute_dest_amount",
        store=True)

    @api.depends("amount")
    def _compute_dest_amount(self):
        for line in self:
            line.dest_amount = 0
            if line.location_dest_id.usage == "usage":
                line.dest_amount = abs(line.amount)

    @api.depends("amount")
    def _compute_origin_amount(self):
        for line in self:
            line.origin_amount = 0
            if line.location_id.usage == "internal":
                line.origin_amount = -abs(line.amount)

    @api.depends("quantity_done")
    def _compute_dest_qty(self):
        for line in self:
            line.dest_qty = 0
            if line.location_dest_id.usage == "internal":
                line.dest_qty = abs(line.quantity_done)

    @api.depends("quantity_done")
    def _compute_origin_qty(self):
        for line in self:
            line.origin_qty = 0
            if line.location_id.usage == "internal":
                line.origin_qty = -abs(line.quantity_done)
