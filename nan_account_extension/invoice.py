# -*- encoding: latin-1 -*-
##############################################################################
#
# Copyright (c) 2010 NaN Projectes de Programari Lliure, S.L. All Rights Reserved.
#                    http://www.NaN-tic.com
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

import netsvc
from osv import osv
from osv import fields
from tools.translate import _
import psycopg2

class account_invoice(osv.osv):
    _inherit = 'account.invoice'

    def _check_invoice_number_date(self, cr, uid, ids):
        for invoice in self.browse(cr, uid, ids):
            if invoice.number and invoice.number != '/' and invoice.date_invoice and invoice.journal_id.check_invoice_number_date:
                cr.execute("""
                    SELECT 
                        number, 
                        date_invoice
                    FROM
                        account_invoice
                    WHERE
                        journal_id = %s and (
                        ( number < %s and date_invoice > %s ) or
                        ( number > %s and date_invoice < %s )
                        )
                        """, (invoice.journal_id.id, invoice.number, invoice.date_invoice, invoice.number, invoice.date_invoice) )
                records = cr.fetchall()
                if records:
                    limit = 10
                    records = [_('Number: %s, Date: %s') % (record[0], record[1]) for record in records]
                    text = '\n'.join( records[:limit] )
                    if len(records) > limit:
                        text += '\n...'
                    raise osv.except_osv( _('Error!'), _('Journal %(journal)s is configured to check invoice numbers and dates but the check failed.\n\nYou are trying to create invoice %(invoice_number)s with date %(invoice_date)s but %(invoice_count)d invoices exist which have incompatible numbers and dates:\n\n%(invoices)s') % {
                        'journal': invoice.journal_id.name, 
                        'invoice_number': invoice.number, 
                        'invoice_date': invoice.date_invoice, 
                        'invoice_count': len(records),
                        'invoices': text,
                        })
        return True 

    _constraints = [ (_check_invoice_number_date, 'Invoice date is previous to an existing invoice.', ['number','date_invoice']) ]

    def onchange_payment_term(self, cr, uid, ids, payment_term, context):
        if payment_term:
            return {
                'value': {
                    'date_due': False,
                }
            }
        return {}

    def write(self, cr, uid, ids, vals, context=None):
        #mod dani
        if vals.has_key('date_due'):
            if vals['date_due'] == '':
                vals.pop("date_due", None)
        #end mod dani     
        result = super(account_invoice, self).write(cr, uid, ids, vals, context)
        if vals.get('state') == 'open':
            for invoice in self.browse(cr, uid, ids, context):
                if not invoice.type in ('in_invoice','in_refund'):
                    continue
                domain = []
                domain.append( ('partner_id','=',invoice.partner_id.id) )
                domain.append( ('type','=',invoice.type) )
                domain.append( ('date_invoice', '=', invoice.date_invoice) )
                domain.append( ('reference', '=', invoice.reference) )
                domain.append( ('state','in', ('open','done')) )
                invoice_ids = self.search(cr, uid, domain, context=context)
                if len(invoice_ids) > 1:
                    text = []
                    for invoice in self.browse(cr, uid, invoice_ids, context):
                        text.append( _('Partner: %s\nInvoice Reference: %s') % ( invoice.partner_id.name, invoice.reference ) )
                    text = '\n\n'.join( text )
                    raise osv.except_osv( _('Validation Error'), _('The following supplier invoices have duplicated information:\n\n%s') % text)
        return result

    def inv_line_characteristic_hashcode(self, invoice, invoice_line):
        if invoice.journal_id.group_products:
            value = "%s-%s-%s-%s"%(
                invoice_line['account_id'],
                invoice_line.get('tax_code_id','False'),
                invoice_line.get('analytic_account_id','False'),
                invoice_line.get('date_maturity','False'))
            if invoice.journal_id.group_products_text:
                invoice_line['name'] = invoice.journal_id.group_products_text
            return value
        return super(account_invoice, self).inv_line_characteristic_hashcode(invoice, invoice_line)

account_invoice()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

