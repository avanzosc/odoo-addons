# -*- coding: utf-8 -*-
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api


class StockQuantMove(models.TransientModel):
    _inherit = 'stock.quant.move'

    picking_id = fields.Many2one(
        comodel_name='stock.picking', string='Picking')

    @api.model
    def default_get(self, fields):
        res = super(StockQuantMove, self).default_get(fields)
        if self.env.context.get('picking_id', False):
            res = self._catch_product_default_location(res)
        return res

    def _catch_product_default_location(self, res):
        quant_obj = self.env['stock.quant']
        res['picking_id'] = self.env.context.get('picking_id')
        pack = []
        lines = res.get('pack_move_items', False)
        for line in lines:
            if line.get('quant', False):
                quant = quant_obj.browse(line.get('quant'))
                if not quant.reservation_id:
                    line['dest_loc'] = (
                        quant.product_id.default_location.id or
                        quant.product_id.categ_id.default_location.id or
                        False)
                    pack.append(line)
        res['pack_move_items'] = pack
        return res

    @api.one
    def do_transfer(self):
        res = super(StockQuantMove, self).do_transfer()
        if self.picking_id:
            self.picking_id.relocation_made = True
        return res


class StockQuantMoveItems(models.TransientModel):
    _inherit = 'stock.quant.move_items'
    _description = 'Picking wizard items'

    dest_loc = fields.Many2one(required=False)
