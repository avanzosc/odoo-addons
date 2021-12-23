# Copyright 2021 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api


class StockPickingBatch(models.Model):
    _inherit = 'stock.picking.batch'

    move_ids = fields.One2many(
        string="Stock moves", comodel_name='stock.move',
        compute='_compute_move_ids')
    move_line_ids = fields.One2many(
        string='Stock move lines', comodel_name='stock.move.line',
        compute='_compute_move_ids', inverse='_set_move_line_ids',
        readonly=True,
        states={'draft': [('readonly', False)],
                'in_progress': [('readonly', False)]})
    show_check_availability = fields.Boolean(
        compute='_compute_move_ids')

    @api.depends('picking_ids', 'picking_ids.move_line_ids',
                 'picking_ids.move_lines', 'picking_ids.move_lines.state')
    def _compute_move_ids(self):
        for batch in self:
            stock_moves = self.env['stock.move']
            stock_move_lines = self.env['stock.move.line']
            for picking in batch.picking_ids:
                stock_moves += picking.move_lines
                stock_move_lines += picking.move_line_ids
            batch.move_ids = stock_moves
            batch.move_line_ids = stock_move_lines
            batch.show_check_availability = any(
                m.state not in ['assigned', 'done'] for m in batch.move_ids)

    def _set_move_line_ids(self):
        new_move_lines = self[0].move_line_ids
        for picking in self.picking_ids:
            old_move_lines = picking.move_line_ids
            picking.move_line_ids = new_move_lines.filtered(
                lambda ml: ml.picking_id.id == picking.id)
            move_lines_to_unlink = old_move_lines - new_move_lines
            if move_lines_to_unlink:
                move_lines_to_unlink.unlink()
