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

import decimal_precision as dp
from tools.translate import _

from osv import osv
from osv import fields

class wiz_crear_factura(osv.osv_memory):
    _name = 'wiz.crear.factura'
    _description = 'Asistente para crear las facturas'
 
    _columns = {
        'partner_id': fields.many2one('res.partner', 'Empresa', readonly=True),
        'journal_id': fields.many2one('account.journal', 'Diario'),
        'description': fields.char('Descripción', size=64),
        'importe': fields.float('Importe', digits_compute=dp.get_precision('Account')),
    }
    
    def button_create_inv(self, cr, uid, ids, context=None):
        invoice_obj = self.pool.get('account.invoice')
        invoice_line_obj = self.pool.get('account.invoice.line')
        address_obj = self.pool.get('res.partner.address')
        for wiz in self.browse(cr, uid, ids):
            address = address_obj.search(cr, uid, [('partner_id', '=', wiz.partner_id.id)])
            if address:
                values = {
                    'name': 'Prev: '+ wiz.description,
                    'partner_id': wiz.partner_id.id,
                    'journal_id': wiz.journal_id.id,
                    'address_invoice_id': address[0].id,
                    'account_id': wiz.partner_id.property_account_receivable.id,
                }
                if wiz.partner_id.property_payment_term:
                    values.update({'payment_term': wiz.partner_id.property_payment_term.id})
                if wiz.partner_id.payment_type_customer:
                    values.update({'payment_type': wiz.partner_id.payment_type_customer.id})
                if wiz.partner_id.property_account_position:
                    values.update({'fiscal_position': wiz.partner_id.property_account_position.id})
            else:
                raise osv.except_osv(_('Error!'),_('Address not found for Partner: '), wiz.partner_id.name)
            
            invoice_id = invoice_obj.create(cr, uid, values)
        return True
    
wiz_crear_factura()