# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.depends('procurement_group_id',
                 'procurement_group_id.procurement_ids',
                 'procurement_group_id.procurement_ids.state')
    @api.multi
    def _compute_shipped(self):
        for sale in self:
            group = sale.procurement_group_id
            val = False
            if group:
                val = all([proc.state in ['cancel', 'done'] for proc in
                           group.procurement_ids])
            sale.shipped = val

    @api.depends('invoice_ids', 'invoice_ids.state', 'state')
    @api.multi
    def _compute_invoiced(self):
        for sale in self:
            val = True
            if (not sale.invoice_ids.filtered(lambda x: x.state != 'cancel') or
                    sale.state == 'manual' or sale.invoice_ids.filtered(
                    lambda x: x.state not in ('paid', 'cancel'))):
                val = False
            sale.invoiced = val

    shipped = fields.Boolean(compute='_compute_shipped', method=False,
                             string='Delivered', store=True)
    invoiced = fields.Boolean(compute='_compute_invoiced', method=False,
                              string='Paid', store=True)

    def __init__(self, pool, cr):
        super(SaleOrder, self).__init__(pool, cr)
        for model, store in pool._store_function.iteritems():
            pool._store_function[model] = [
                x for x in store if x[0] != 'sale.order' and
                x[1] != 'shipped' and x[1] != 'invoiced']
