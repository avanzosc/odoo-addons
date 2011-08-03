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

from osv import osv, fields
import decimal_precision as dp
from tools.translate import _
    

class res_partner(osv.osv):
    _inherit = 'res.partner'
    
    _columns = {
            'disc1' : fields.float('Discount 1', size=14, help = '% Specific Client Discount'),
            'disc2' : fields.float('Discount 2', size=14, help = '% Specific Client Discount'),
            'disc3' : fields.float('Discount 3', size=14, help = '% Specific Client Discount'),
    }
    
    _defaults = {  
        'disc1': lambda *a: 0,
        'disc2': lambda *a: 0,
        'disc3': lambda *a: 0,
    }
res_partner()

class account_invoice_tax(osv.osv):
    _inherit = 'account.invoice.tax'
 
    _columns = {
            'disc' : fields.float('Discounted', size=14),
            'disc1' : fields.float('Disc 1', size=14, help = '% Specific Client Discount'),
            'disc2' : fields.float('Disc 2', size=14, help = '% Specific Client Discount'),
            'disc3' : fields.float('Disc 3', size=14, help = '% Specific Client Discount'),
    }
    
    _defaults = {  
        'disc1': lambda *a: 0,
        'disc2': lambda *a: 0,
        'disc3': lambda *a: 0,
    }
    
account_invoice_tax()

class account_invoice(osv.osv):
    _inherit = 'account.invoice'
    
    def _amount_all(self, cr, uid, ids, name, args, context=None):
        res = {}
        for invoice in self.browse(cr, uid, ids, context=context):
            res[invoice.id] = {
                'amount_untaxed': 0.0,
                'amount_tax': 0.0,
                'amount_total': 0.0,
                'discounted': 0.0
            }
            for line in invoice.invoice_line:
                res[invoice.id]['amount_untaxed'] += line.price_subtotal
            if invoice.tax_line:
                res[invoice.id]['discounted'] = res[invoice.id]['amount_untaxed'] - res[invoice.id]['amount_untaxed'] * invoice.tax_line[0].disc1 / 100
                res[invoice.id]['discounted'] = res[invoice.id]['discounted'] - res[invoice.id]['discounted'] * invoice.tax_line[0].disc2 / 100
                res[invoice.id]['discounted'] = res[invoice.id]['discounted'] - res[invoice.id]['discounted'] * invoice.tax_line[0].disc3 / 100
            for line in invoice.tax_line:
                res[invoice.id]['amount_tax'] += line.amount
            if res[invoice.id]['discounted'] != 0:
                res[invoice.id]['amount_total'] = res[invoice.id]['amount_tax'] + res[invoice.id]['discounted']
            else:
                res[invoice.id]['amount_total'] = res[invoice.id]['amount_tax'] + res[invoice.id]['amount_untaxed']
        return res
    
    def _get_invoice_tax(self, cr, uid, ids, context=None):
        account = self.pool.get('account.invoice')
        return super(account_invoice, account)._get_invoice_tax(cr, uid, ids, context)
    
    def _get_invoice_line(self, cr, uid, ids, context=None):
        account = self.pool.get('account.invoice')
        return super(account_invoice, account)._get_invoice_line(cr, uid, ids, context)
    
    _columns = {
           'discounted': fields.function(_amount_all, method=True, digits_compute=dp.get_precision('Account'), string='Discounted',
                store={
                    'account.invoice': (lambda self, cr, uid, ids, c={}: ids, ['invoice_line'], 20),
                    'account.invoice.tax': (_get_invoice_tax, None, 20),
                    'account.invoice.line': (_get_invoice_line, ['price_unit','invoice_line_tax_id','quantity','discount','invoice_id'], 20),
                },
                multi='all'),
           'amount_untaxed': fields.function(_amount_all, method=True, digits_compute=dp.get_precision('Account'), string='Untaxed',
                store={
                    'account.invoice': (lambda self, cr, uid, ids, c={}: ids, ['invoice_line'], 20),
                    'account.invoice.tax': (_get_invoice_tax, None, 20),
                    'account.invoice.line': (_get_invoice_line, ['price_unit','invoice_line_tax_id','quantity','discount','invoice_id'], 20),
                },
                multi='all'),
            'amount_tax': fields.function(_amount_all, method=True, digits_compute=dp.get_precision('Account'), string='Tax',
                store={
                    'account.invoice': (lambda self, cr, uid, ids, c={}: ids, ['invoice_line'], 20),
                    'account.invoice.tax': (_get_invoice_tax, None, 20),
                    'account.invoice.line': (_get_invoice_line, ['price_unit','invoice_line_tax_id','quantity','discount','invoice_id'], 20),
                },
                multi='all'),
            'amount_total': fields.function(_amount_all, method=True, digits_compute=dp.get_precision('Account'), string='Total',
                store={
                    'account.invoice': (lambda self, cr, uid, ids, c={}: ids, ['invoice_line'], 20),
                    'account.invoice.tax': (_get_invoice_tax, None, 20),
                    'account.invoice.line': (_get_invoice_line, ['price_unit','invoice_line_tax_id','quantity','discount','invoice_id'], 20),
                },
                multi='all'),
    }
    
    def onchange_partner_id(self, cr, uid, ids, type, partner_id,\
            date_invoice=False, payment_term=False, partner_bank_id=False, company_id=False):
        result = {}
        result = super(account_invoice, self).onchange_partner_id(cr, uid, ids, type, partner_id, date_invoice, payment_term, partner_bank_id, company_id)
        for account in self.browse(cr, uid, ids):
            for taxe in account.tax_line:
                self.pool.get('account.invoice.tax').write(cr, uid, taxe.id, {'disc1': account.partner_id.disc1, 'disc2': account.partner_id.disc2, 'disc3': account.partner_id.disc3})
        return result
    
    def button_reset_taxes(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        ctx = context.copy()
        ait_obj = self.pool.get('account.invoice.tax')
        tax_obj = self.pool.get('account.tax')
        for id in ids:
            inv = self.browse(cr, uid, id)
            if inv.tax_line:
                for tax_line in self.browse(cr, uid, id).tax_line:
                    disc = {
                        'disc1': tax_line.disc1,
                        'disc2': tax_line.disc2,
                        'disc3': tax_line.disc3,
                    }
            else:
                 disc = {
                        'disc1': inv.partner_id.disc1,
                        'disc2': inv.partner_id.disc2,
                        'disc3': inv.partner_id.disc3,
                    }
            cr.execute("DELETE FROM account_invoice_tax WHERE invoice_id=%s AND manual is False", (id,))
            partner = self.browse(cr, uid, id, context=ctx).partner_id
            if partner.lang:
                ctx.update({'lang': partner.lang})
            for taxe in ait_obj.compute(cr, uid, id, context=ctx).values():
                if disc['disc1'] > 0:
                    taxe['disc'] = taxe['base'] - taxe['base'] * disc['disc1'] / 100
                    taxe['disc1'] = disc['disc1']
                    if disc['disc2'] > 0:
                        taxe['disc'] = taxe['disc'] - taxe['disc'] * disc['disc2'] / 100
                        taxe['disc2'] = disc['disc2']
                        if disc['disc3'] > 0:
                            taxe['disc'] = taxe['disc'] - taxe['disc'] * disc['disc3'] / 100
                            taxe['disc3'] = disc['disc3']
                tax = tax_obj.browse(cr, uid, tax_obj.search(cr, uid, [('name', '=', taxe['name'])]))
                if taxe['disc'] != 0:
                    taxe['amount'] = taxe['disc'] * tax[0].amount
                else:
                    taxe['amount'] = taxe['base'] * tax[0].amount
                ait_obj.create(cr, uid, taxe)
                
        # Update the stored value (fields.function), so we write to trigger recompute
        self.pool.get('account.invoice').write(cr, uid, ids, {'invoice_line':[]}, context=ctx)
        return True

account_invoice()