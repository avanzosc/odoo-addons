# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, api


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.model
    def _prepare_procurement_from_move(self, move):
        res = super(StockMove, self)._prepare_procurement_from_move(move)
        if move.procurement_id and move.procurement_id.sale_line_id:
            find_routes = [self.env.ref('stock.route_warehouse0_mto').id,
                           self.env.ref('purchase.route_warehouse0_buy').id]
            routes = move.product_id.route_ids.filtered(
                lambda r: r.id in find_routes)
            if move.product_id.type == 'service' and len(routes) == 2:
                res['sale_line_id'] = move.procurement_id.sale_line_id.id
        return res
