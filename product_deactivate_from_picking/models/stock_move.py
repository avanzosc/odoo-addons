# -*- coding: utf-8 -*-
# Copyright 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.multi
    def action_done(self):
        res = super(StockMove, self).action_done()
        for move in self.filtered(
            lambda x: x.state == 'done' and x.picking_id and
                x.picking_type_id.code == 'outgoing' and
                x.product_id.active and x.product_id.unique):
            if move.product_id.qty_available <= 0:
                move.product_id.set_as_deactivated_from_picking(
                    move.picking_id)
        for move in self.filtered(
            lambda x: x.state == 'done' and x.picking_id and
                x.picking_type_id.code == 'incoming' and not
                x.product_id.active and x.product_id.unique and
                x.origin_returned_move_id):
            if move.product_id.qty_available >= 0:
                move.product_id.set_as_activated_from_picking(
                    move.picking_id)
        return res
