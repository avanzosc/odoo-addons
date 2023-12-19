# Copyright 2019 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    imei = fields.Char(string="imei")


class StockMove(models.Model):
    _inherit = "stock.move"

    def _action_done(self):
        res = super()._action_done()
        for line in res.mapped('move_line_ids').filtered(
                lambda l: l.imei and l.lot_id):
            line.lot_id.imei = line.imei
        return res

    def _prepare_move_line_vals(self, quantity=None, reserved_quant=None):
        vals = super()._prepare_move_line_vals(
            quantity=quantity, reserved_quant=reserved_quant)
        if reserved_quant:
            vals = dict(
                vals,
                imei=reserved_quant.lot_id.imei,
            )
        return vals
