# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc - Advanced Open Source Consulting
#    Copyright (C) 2011 - 2014 Avanzosc <http://www.avanzosc.com>
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

from osv import osv
from osv import fields
from datetime import datetime

class create_incurrent_payment_order(osv.osv_memory):
    _name = 'create.incurrent.payment.order'
    
    
    _columns = {
                'start_date':fields.date('Start date'),
                'end_date':fields.date('End date'),
                'get_relaunched':fields.boolean('Allow re-launched'),
                'payment_mode_id': fields.many2one('payment.mode', 'Payment Mode'),
                }
    
    def create_payment_order(self, cr, uid, ids ,context=None):
        
        
        order_obj = self.pool.get('payment.order')
        line_obj = self.pool.get('account.move.line')
        invoice_obj = self.pool.get('account.invoice')
        return_line_obj = self.pool.get('setitria.fitxerretornat.line')
        return_obj = self.pool.get('setitria.fitxerretornat')
        payment_res = {}
        
        # move_ids = los asientos contables basados en las devoluciones incorrientes
        move_ids = []
        
        
        wiz = self.browse(cr,uid,ids)
        if isinstance(wiz,list):
            wiz = wiz[0]
            
        invoice_ids = []
        if wiz.get_relaunched:
            invoice_ids = invoice_obj.search(cr,uid,[('state', '=', 'unpaid')])
        else:
            invoice_ids = invoice_obj.search(cr,uid,[('state', '=', 'unpaid'),('last_relaunch_date', '=', False)])
        
        return_line_ids = return_line_obj.search(cr,uid,[('date', '>=', wiz.start_date),('date', '<=', wiz.end_date),('invoice_id', 'in', invoice_ids),('motiu_dev','=', '1')])
        return_line_os = return_line_obj.browse(cr,uid,return_line_ids)
        for return_line in return_line_os:
            if not return_line.invoice_id.move_id.id in move_ids:
                move_ids.append(return_line.invoice_id.move_id.id)
        payment_vals = {'type':'receivable',
                        'mode':wiz.payment_mode_id.id,
                        'state':'draft',
                        'incurrent_payment':True,
                        'date_prefered':'due',
                        'create_account_moves':'bank-statement',
                        'reference': self.pool.get('ir.sequence').get(cr, uid, 'rec.payment.order'),
                        }
        payment_id = order_obj.create(cr,uid,payment_vals)
        cr.commit()
        payment = order_obj.browse(cr,uid,payment_id)
        # Search for move line to pay:
        domain = [('reconcile_id', '=', False),('account_id.type', '=', payment.type),('amount_to_pay', '<>', 0)]
        
        if payment.mode:
            domain += [('payment_type','=',payment.mode.type.id)]
    
        domain += [('move_id','in',move_ids)]
        if move_ids:
#        line_ids = line_obj.search(cr, uid, domain, order='date_maturity', context=context)
            query = "select id from account_move_line aml where aml.move_id in " + str(tuple(move_ids)) + " and aml.credit - aml.debit != 0 and aml.reconcile_id is null and aml.account_id in (select id from account_account where type = 'receivable')"     
            cr.execute(query)
            vals = cr.fetchall()
            for (line_id, ) in vals :
                line = line_obj.browse(cr, uid, line_id, context=context)
                date_to_pay = line.date_maturity
                amount_to_pay = -line.amount_to_pay
                
                self.pool.get('payment.line').create(cr,uid,{
                    'move_line_id': line.id,
                    'amount_currency': amount_to_pay,
                    'bank_id': self.pool.get('account.move.line').line2bank(cr, uid, [line_id], wiz.payment_mode_id.id, context).get(line.id),
                    'order_id': payment.id,
                    'partner_id': line.partner_id and line.partner_id.id or False,
                    'communication': (line.ref and line.name!='/' and line.ref+'. '+line.name) or line.ref or line.name or '/',
                    'date': date_to_pay,
                    'currency': line.invoice and line.invoice.currency_id.id or False,
                    'account_id': line.account_id.id,
                    }, context=context)
                cr.commit()
            payment_res.update({'type': 'ir.actions.act_window',
                                'res_model': 'payment.order',
                                'view_type': 'form',
                                'view_mode': 'form,tree',
                                'res_id':payment.id,
                                'target': 'current',
                                'context':context})
        return payment_res
create_incurrent_payment_order()