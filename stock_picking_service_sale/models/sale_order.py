# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, api


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    @api.multi
    def action_ship_create(self):
        res = super(SaleOrder, self).action_ship_create()
        picking = self.env['stock.picking'].search(
            [('group_id', '=', self.procurement_group_id.id)])
        picking.get_service_lines(self)
        return res


class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    @api.multi
    def invoice_line_create(self):
        if self.env.context.get('not_create_service', False):
            return super(SaleOrderLine,
                         self.filtered(lambda x: x.product_id.type !=
                                       'service')).invoice_line_create()
        return super(SaleOrderLine, self).invoice_line_create()
