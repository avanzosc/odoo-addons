# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc - Avanced Open Source Consulting
#    Copyright (C) 2011 - 2012 Avanzosc <http://www.avanzosc.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

import time

from crm import crm
from osv import fields, osv
from tools.translate import _

class crm_opportunity(osv.osv):
    _inherit = 'crm.lead'
    
    _columns = {
        'credit': fields.float('Total Receivable'),
        'invoice2pay': fields.integer('Invoices to pay'),
        'last_invoice': fields.date('Last Invoice'),
        'last_payment': fields.date('Last Payment'),
    }
    
    def onchange_partner_id(self, cr, uid, ids, part, email=False):
        invoice_obj = self.pool.get('account.invoice')
        voucher_obj = self.pool.get('account.voucher')
        res = super(crm_opportunity, self).onchange_partner_id(cr, uid, ids, part, email)
        if part:
            partner = self.pool.get('res.partner').browse(cr, uid, part)
            unpaid_invoice_ids = invoice_obj.search(cr, uid, [('partner_id', '=', part), ('state', '=', 'open')])
            invoice_ids = invoice_obj.search(cr, uid, [('partner_id', '=', part)])
            voucher_ids = voucher_obj.search(cr, uid, [('partner_id', '=', part)])
            if invoice_ids:
                last_invoice = invoice_obj.browse(cr, uid, invoice_ids[0])
                for invoice in invoice_obj.browse(cr, uid, invoice_ids):
                    if invoice.date_invoice > last_invoice.date_invoice and invoice.date_invoice != False:
                        last_invoice = invoice
                    elif last_invoice.date_invoice == False:
                        last_invoice = invoice
                res['value'].update({
                       'last_invoice': last_invoice.date_invoice,
                })  
            if voucher_ids:
                last_voucher = voucher_obj.browse(cr, uid, voucher_ids[0])
                for voucher in voucher_obj.browse(cr, uid, voucher_ids):
                    if voucher.date > last_voucher.date and voucher.date != False:
                        last_voucher = voucher
                    elif last_voucher.date == False:
                        last_voucher = voucher
                res['value'].update({
                       'last_payment': last_voucher.date,
                })            
            res['value'].update({
                'credit': partner.credit,
                'invoice2pay': int(len(unpaid_invoice_ids)),
            })
        return res
    
crm_opportunity()

class crm_make_sale(osv.osv_memory):

    _inherit = "crm.make.sale"
    
    def makeOrder(self, cr, uid, ids, context=None):
        """
        This function  create Quotation on given case.
        @param self: The object pointer
        @param cr: the current row, from the database cursor,
        @param uid: the current user’s ID for security checks,
        @param ids: List of crm make sales' ids
        @param context: A standard dictionary for contextual values
        @return: Dictionary value of created sales order.
        """
        if context is None:
            context = {}

        case_obj = self.pool.get('crm.lead')
        sale_obj = self.pool.get('sale.order')
        partner_obj = self.pool.get('res.partner')
        address_obj = self.pool.get('res.partner.address')
        data = context and context.get('active_ids', []) or []

        for make in self.browse(cr, uid, ids, context=context):
            partner = make.partner_id
            partner_addr = partner_obj.address_get(cr, uid, [partner.id],
                    ['default', 'invoice', 'delivery', 'contact'])
            pricelist = partner.property_product_pricelist.id
            fpos = partner.property_account_position and partner.property_account_position.id or False
            new_ids = []
            for case in case_obj.browse(cr, uid, data, context=context):
                if not partner and case.partner_id:
                    partner = case.partner_id
                    fpos = partner.property_account_position and partner.property_account_position.id or False
                    partner_addr = partner_obj.address_get(cr, uid, [partner.id],
                            ['default', 'invoice', 'delivery', 'contact'])
                    pricelist = partner.property_product_pricelist.id
                if False in partner_addr.values():
                    raise osv.except_osv(_('Data Insufficient!'), _('Customer has no addresses defined!'))
                
                def_address = address_obj.browse(cr, uid, partner_addr['default'])
                
                if not def_address.analytic:
                    raise osv.except_osv(_('Data Insufficient!'), _('Customer has no analytic account defined!'))
                vals = {
                    'origin': _('Opportunity: %s') % str(case.id),
                    'section_id': case.section_id and case.section_id.id or False,
                    'shop_id': make.shop_id.id,
                    'partner_id': partner.id,
                    'pricelist_id': pricelist,
                    'partner_invoice_id': partner_addr['invoice'],
                    'partner_order_id': partner_addr['contact'],
                    'partner_shipping_id': partner_addr['delivery'],
                    'project_id': def_address.analytic and def_address.analytic.id or False,
                    'date_order': time.strftime('%Y-%m-%d'),
                    'fiscal_position': fpos,
                }
                if partner.id:
                    vals['user_id'] = partner.user_id and partner.user_id.id or uid
                new_id = sale_obj.create(cr, uid, vals)
                case_obj.write(cr, uid, [case.id], {'ref': 'sale.order,%s' % new_id})
                new_ids.append(new_id)
                message = _('Opportunity ') + " '" + case.name + "' "+ _("is converted to Quotation.")
                self.log(cr, uid, case.id, message)
                case_obj._history(cr, uid, [case], _("Converted to Sales Quotation(id: %s).") % (new_id))

            if make.close:
                case_obj.case_close(cr, uid, data)
            if not new_ids:
                return {'type': 'ir.actions.act_window_close'}
            if len(new_ids)<=1:
                value = {
                    'domain': str([('id', 'in', new_ids)]),
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'sale.order',
                    'view_id': False,
                    'type': 'ir.actions.act_window',
                    'res_id': new_ids and new_ids[0]
                }
            else:
                value = {
                    'domain': str([('id', 'in', new_ids)]),
                    'view_type': 'form',
                    'view_mode': 'tree,form',
                    'res_model': 'sale.order',
                    'view_id': False,
                    'type': 'ir.actions.act_window',
                    'res_id': new_ids
                }
            return value
    
crm_make_sale()