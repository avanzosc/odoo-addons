# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.multi
    def _prepare_invoice_line(self, qty):
        values = super(SaleOrderLine, self)._prepare_invoice_line(qty)
        cond = [('sale_line_id', '=', self.id)]
        moves = self.env['stock.move'].search(cond)
        for move in moves:
            cond = [('move_id', '=', move.id),
                    ('product_id', '=', self.product_id.id),
                    ('state', '=', 'done')]
            lines = self.env['stock.move.line'].search(cond).filtered(
                lambda c: c.lot_id)
            if lines:
                values['lot_ids'] = [(6, 0, lines.mapped('lot_id').ids)]
        return values
