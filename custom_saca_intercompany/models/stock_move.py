# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    saca_line_id = fields.Many2one(
        string="Saca Line",
        comodel_name="saca.line",
        compute='_compute_saca_line_id',
        store=True)
    saca_id = fields.Many2one(
        string="Saca",
        comodel_name="saca",
        related="saca_line_id.saca_id",
        store=True)

    @api.depends("purchase_line_id", "sale_line_id")
    def _compute_saca_line_id(self):
        for move in self:
            if move.purchase_line_id:
                move.saca_line_id = move.purchase_line_id.saca_line_id.id
            else:
                move.saca_line_id = move.sale_line_id.saca_line_id.id
