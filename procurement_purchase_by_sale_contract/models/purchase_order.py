# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    sale_contract = fields.Many2one(
        'account.analytic.account', string='Sale contract')

    @api.model
    def create(self, vals):
        if 'sale_contract' in self.env.context:
            vals.update({'sale_contract':
                         self.env.context.get('sale_contract').id})
        return super(PurchaseOrder, self).create(vals)

    def search(self, cr, uid, args, offset=0, limit=None, order=None,
               context=None, count=False):
        if context and 'sale_contract' in context:
            args.append(('sale_contract', '=',
                         context.get('sale_contract').id))
        return super(PurchaseOrder, self).search(
            cr, uid, args, offset=offset, limit=limit, order=order,
            context=context, count=count)
