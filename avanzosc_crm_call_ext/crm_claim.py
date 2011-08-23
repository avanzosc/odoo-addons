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

from crm import crm
from osv import fields, osv

class crm_claim(crm.crm_case, osv.osv):
    _inherit = 'crm.claim'
    
    _columns = {
        'credit': fields.float('Total Receivable'),
        'invoice2pay': fields.integer('Invoices to pay'),
        'last_invoice': fields.date('Last Invoice'),
        'last_payment': fields.date('Last Payment'),
    }
    
    def onchange_partner_id(self, cr, uid, ids, part, email=False):
        invoice_obj = self.pool.get('account.invoice')
        voucher_obj = self.pool.get('account.voucher')
        res = super(crm_claim, self).onchange_partner_id(cr, uid, ids, part, email)
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
    
crm_claim()