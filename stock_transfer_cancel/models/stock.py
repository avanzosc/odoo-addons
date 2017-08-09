# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, api, exceptions, _


class StockQuant(models.Model):

    _inherit = 'stock.quant'

    @api.multi
    def revert(self, move):
        vals = {
            'location_id': move.location_id.id,
            'history_ids': [(3, move.id)],
            'reservation_id': False,
            'package_id': False,
        }
        self.sudo().write(vals)


class StockMove(models.Model):

    _inherit = 'stock.move'

    @api.multi
    def revert_quants(self):
        for record in self:
            record.mapped('quant_ids').revert(record)

    @api.multi
    def clean_negative_quants(self):
        self.ensure_one()
        delete_quants = self.env['stock.quant']
        negative_quants = self.mapped('quant_ids').filtered(
            lambda x: x.qty < 0 and x.location_id == self.location_id)
        for negative_quant in negative_quants:
            negative_propagated = self.mapped('quant_ids').filtered(
                lambda x: x.propagated_from_id.id == negative_quant.id and
                x.location_id == self.location_dest_id)
            if negative_propagated:
                delete_quants |= negative_propagated
                delete_quants |= negative_quant
        if delete_quants:
            delete_quants.with_context(force_unlink=True).sudo().unlink()

    @api.multi
    def action_cancel(self):
        for move in self.filtered(lambda x: x.state == 'done'):
            move.clean_negative_quants()
            if any(move.mapped('quant_ids').filtered(
                    lambda x: x.qty > 0 and x.location_id !=
                    move.location_dest_id)):
                raise exceptions.Warning(
                    _('Operation Forbidden! You cannot cancel a stock move '
                      'that has been set to \'Done\' and it has been moved '
                      'afterwards.'))
            move.revert_quants()
            move.write({'state': 'confirmed'})
            super(StockMove, move).action_cancel()
        not_done_moves = self.filtered(lambda x: x.state != 'done')
        return not_done_moves and super(StockMove, not_done_moves
                                        ).action_cancel() or True
