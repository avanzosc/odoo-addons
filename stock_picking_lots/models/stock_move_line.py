# Copyright 2019 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    imei = fields.Char(
        string="imei",
    )
    lot_ref = fields.Char(
        string="Lot Internal Reference",
    )

    @api.onchange("lot_name", "lot_id")
    def onchange_serial_number(self):
        result = super(StockMoveLine, self).onchange_serial_number()
        if self.lot_id:
            self.imei = self.lot_id.imei if self.lot_id.imei else self.imei
            self.lot_ref = self.lot_id.ref if self.lot_id.ref else self.lot_ref
        return result


class StockMove(models.Model):
    _inherit = "stock.move"

    def _action_done(self):
        res = super()._action_done()
        for line in res.mapped("move_line_ids").filtered(
                lambda l: (l.imei or l.lot_ref) and l.lot_id):
            if line.imei:
                line.lot_id.imei = line.imei
            if line.lot_ref:
                line.lot_id.ref = line.lot_ref
        return res

    def _prepare_move_line_vals(self, quantity=None, reserved_quant=None):
        vals = super()._prepare_move_line_vals(
            quantity=quantity, reserved_quant=reserved_quant)
        if reserved_quant:
            vals = dict(
                vals,
                imei=reserved_quant.lot_id.imei,
                lot_ref=reserved_quant.lot_id.ref,
            )
        return vals
