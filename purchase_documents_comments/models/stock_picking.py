# -*- coding: utf-8 -*-
# Copyright 2018 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import api, models, fields


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    purchase_comment = fields.Text(string='Purchase internal comments')
    purchase_propagated_comment = fields.Text(
        string='Purchase propagated internal comments')

    @api.multi
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        for picking in self:
            picking_com, picking_pcom = (
                picking.partner_id._get_supplier_picking_comments())
            picking.purchase_comment = picking_com
            picking.purchase_propagated_comment = picking_pcom

    @api.model
    def _create_invoice_from_picking(self, picking, values):
        purchase_comment = values.get('purchase_comment', '')
        pcomment_list = []
        if purchase_comment:
            pcomment_list.append(purchase_comment)
        if picking.purchase_propagated_comment:
            pcomment_list.append(picking.purchase_propagated_comment
                                 )
        partner_id = values.get('partner_id')
        if partner_id:
            partner = self.env['res.partner'].browse(partner_id)
            if partner._get_supplier_invoice_comments():
                pcomment_list.append(partner._get_supplier_invoice_comments())
        values['purchase_comment'] = '\n'.join(pcomment_list)
        return super(StockPicking, self)._create_invoice_from_picking(
            picking, values)
