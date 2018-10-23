# -*- coding: utf-8 -*-
# Copyright 2018 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    comment = fields.Text(string='Internal comments')
    propagated_comment = fields.Text(string='Propagated internal comments')

    @api.model
    def _prepare_invoice(self, order, lines):
        comment_list = []
        res = super(PurchaseOrder, self)._prepare_invoice(order, lines)
        purchase_comment = res.get('purchase_comment')
        partner_id = res.get('partner_id', order.partner_id.id)
        if purchase_comment:
            comment_list.append(purchase_comment)
        if order.propagated_comment:
            comment_list.append(order.propagated_comment)
        if partner_id:
            partner = self.env['res.partner'].browse(partner_id)
            if partner._get_supplier_invoice_comments():
                comment_list.append(partner._get_supplier_invoice_comments())
        res['purchase_comment'] = '\n'.join(comment_list)
        return res

    @api.multi
    def onchange_partner_id(self, partner_id):
        val = super(PurchaseOrder, self).onchange_partner_id(partner_id)
        if partner_id:
            partner = self.env['res.partner'].browse(partner_id)
            comment, pcomment = partner._get_purchase_comments()
            val['value'].update({'comment': comment,
                                 'propagated_comment': pcomment})
        return val
