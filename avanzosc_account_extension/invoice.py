# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time
from lxml import etree
import decimal_precision as dp

import netsvc
import pooler
from osv import fields, osv, orm
from tools.translate import _


class account_invoice(osv.osv):
    _inherit = 'account.invoice'
    
    def _amount_residual_ref(self, cr, uid, ids, name, args, context=None):
        res = {}
        for invoice in self.browse(cr, uid, ids, context=context):
            residual = invoice.residual
            if invoice.type in ('in_refund', 'out_refund'):
                res[invoice.id] = residual * -1
            else:
                res[invoice.id] = residual  
        return res
    
    
    def _amount_untaxed_ref(self, cr, uid, ids, name, args, context=None):
        res = {}
        for invoice in self.browse(cr, uid, ids, context=context):
            untaxed = invoice.amount_untaxed
            if invoice.type in ('in_refund', 'out_refund'):
                res[invoice.id] = untaxed * -1
            else:
                res[invoice.id] = untaxed  
        return res
    
    
    def _amount_all_ref(self, cr, uid, ids, name, args, context=None):
        res = {}
        for invoice in self.browse(cr, uid, ids, context=context):
            amount = invoice.amount_total
            if invoice.type in ('in_refund', 'out_refund'):
                res[invoice.id] = amount * -1
            else:
                res[invoice.id] = amount  
        return res
    
    def _amount_tax_ref(self, cr, uid, ids, name, args, context=None):
        res = {}
        for invoice in self.browse(cr, uid, ids, context=context):
            tax = invoice.amount_tax
            if invoice.type in ('in_refund', 'out_refund'):
                res[invoice.id] = tax * -1
            else:
                res[invoice.id] = tax  
        return res
    
    _columns= {
               'residual_ref':fields.function(_amount_residual_ref, method=True, digits_compute=dp.get_precision('Account'), string='Residual',store=False),
               'amount_untaxed_ref':fields.function(_amount_untaxed_ref, method=True, digits_compute=dp.get_precision('Account'), string='Untaxed',store=False),
               'amount_total_ref':fields.function(_amount_all_ref, method=True, digits_compute=dp.get_precision('Account'), string='Total', store=False),
               'amount_tax_ref':fields.function(_amount_tax_ref, method=True, digits_compute=dp.get_precision('Account'), string='Tax', store=False),
               'origin': fields.char('Source Document', size=500, help="Reference of the document that produced this invoice.", readonly=True, states={'draft':[('readonly',False)]}),
               }
    
    def fields_view_get(self, cr, uid, view_id=None, view_type=False, context=None, toolbar=False, submenu=False):
        res = {}
        journal = False
        if context.has_key('journal_type'):
            journal = context['journal_type']
            if isinstance(journal,(str, unicode)):
                journal=[journal]
            if len(journal) == 1:
                res = super(account_invoice, self).fields_view_get(cr, uid, view_id=view_id, view_type=view_type, context=context, toolbar=toolbar, submenu=submenu)
            else:
                journal_obj = self.pool.get('account.journal')
                if context is None:
                    context = {}
        
                if context.get('active_model', '') in ['res.partner'] and context.get('active_ids', False) and context['active_ids']:
                    partner = self.pool.get(context['active_model']).read(cr, uid, context['active_ids'], ['supplier','customer'])[0]
                    if not view_type:
                        view_id = self.pool.get('ir.ui.view').search(cr, uid, [('name', '=', 'account.invoice.tree')])
                        view_type = 'tree'
                    if view_type == 'form':
                        if partner['supplier'] and not partner['customer']:
                            view_id = self.pool.get('ir.ui.view').search(cr,uid,[('name', '=', 'account.invoice.supplier.form')])
                        else:
                            view_id = self.pool.get('ir.ui.view').search(cr,uid,[('name', '=', 'account.invoice.form')])
                if view_id and isinstance(view_id, (list, tuple)):
                    view_id = view_id[0]
                res = super(account_invoice,self).fields_view_get(cr, uid, view_id=view_id, view_type=view_type, context=context, toolbar=toolbar, submenu=submenu)
        
                type = context.get('journal_type', 'sale')
                for field in res['fields']:
                    if field == 'journal_id':
                        journal_select = journal_obj._name_search(cr, uid, '', [('type', 'in', type)], context=context, limit=None, name_get_uid=1)
                        res['fields'][field]['selection'] = journal_select
        
                if view_type == 'tree':
                    doc = etree.XML(res['arch'])
                    nodes = doc.xpath("//field[@name='partner_id']")
                    partner_string = _('Customer')
                    if context.get('type', 'out_invoice') in ('in_invoice', 'in_refund'):
                        partner_string = _('Supplier')
                    for node in nodes:
                        node.set('string', partner_string)
                    res['arch'] = etree.tostring(doc)
        else:
            res = super(account_invoice, self).fields_view_get(cr, uid, view_id=view_id, view_type=view_type, context=context, toolbar=toolbar, submenu=submenu)
        return res


account_invoice()