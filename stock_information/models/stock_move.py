# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _find_moves_from_stock_information(
        self, company, to_date, from_date=None, category=None, template=None,
            products=None, location_id=None, location_dest_id=None):
        cond = [('company_id', '=', company.id),
                ('date', '<=', to_date),
                ('state', 'not in', ('done', 'cancel'))]
        if from_date:
            cond.append(('date', '>=', from_date))
        if products:
            cond.append(('product_id', 'in', products))
        if location_id:
            cond.append(('location_id', '=', location_id.id))
        if location_dest_id:
            cond.append(('location_dest_id', '=', location_dest_id.id))
        moves = self.search(cond)
        if category:
            moves = moves.filtered(
                lambda x: x.product_id.product_tmpl_id.categ_id.id ==
                category.id)
        if template:
            moves = moves.filtered(
                lambda x: x.product_id.product_tmpl_id.id ==
                template.id)
        return moves
