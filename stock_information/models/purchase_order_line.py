# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models


class PurchaseOrderLine(models.Model):

    _inherit = 'purchase.order.line'

    def _find_purchase_lines_from_stock_information(
            self, company, to_date, product, location, from_date=None):
        cond = [('company_id', '=', company.id),
                ('product_id', '=', product.id),
                ('date_planned', '<=', to_date),
                ('state', '=', 'draft')]
        if from_date:
            cond.append(('date_planned', '>=', from_date))
        purchase_lines = self.search(cond)
        purchase_lines = purchase_lines.filtered(
            lambda x: x.order_id.state not in ('cancel', 'except_picking',
                                               'except_invoice', 'done',
                                               'approved'))
        purchase_lines = purchase_lines.filtered(
            lambda x: x.order_id.picking_type_id.default_location_dest_id.id ==
            location.id)
        return purchase_lines
