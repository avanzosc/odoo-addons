# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.model
    def create(self, vals):
        product_obj = self.env['product.product']
        product = product_obj.browse(vals.get('product_id'))
        route = self.env.ref('procurement_service_project.route_serv_project')
        if (product.type == 'service' and len(product.route_ids) == 1 and
                route.id in product.route_ids.ids):
            return self.env['stock.move']
        move = super(StockMove, self).create(vals)
        return move
