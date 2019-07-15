# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, api


class StockMove(models.Model):

    _inherit = 'stock.move'

    @api.multi
    def _create_line_by_lot(self, invoice_line_vals, lot_id, quants):
        self.ensure_one()
        invoice_line_obj = self.env['account.invoice.line']
        invoice_line_vals['lot_id'] = lot_id.id
        invoice_line_vals['price_unit'] = lot_id.unit_price
        if self.env.context.get('inv_type') in ('in_invoice',
                                                'in_refund'):
            invoice_line_vals['price_unit'] = lot_id.cost_price
        invoice_line_vals['quantity'] = sum(
            quants.filtered(lambda x: x.lot_id.id == lot_id.id).mapped('qty'))
        return invoice_line_obj.create(invoice_line_vals)

    @api.model
    def _create_invoice_line_from_vals(self, move, invoice_line_vals):
        quants = (move.mapped('reserved_quant_ids').filtered(
            lambda x: x.lot_id) | move.mapped('quant_ids').filtered(
            lambda x: x.lot_id))
        if quants:
            line = False
            for lot in quants.mapped('lot_id'):
                vals = invoice_line_vals.copy()
                line = move._create_line_by_lot(vals, lot, quants)
            return line.id
        else:
            return super(StockMove, self)._create_invoice_line_from_vals(
                move, invoice_line_vals)
