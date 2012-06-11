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
import netsvc
from osv import fields, osv
from tools.translate import _
import decimal_precision as dp

class payment_order(osv.osv):
    _name = 'payment.order'
    _inherit = 'payment.order'
    _columns = {
                 'date_done': fields.date('Execution date', readonly=False,states={'done':[('readonly',True)]}),
                }
    def action_open(self, cr, uid, ids, *args):
        res = super(payment_order,self).action_open(cr,uid,ids,*args)
        for order in self.browse(cr, uid, ids):
                date = time.strftime('%Y-%m-%d')
                if order.date_prefered == 'fixed':
                    date = order.date_scheduled 
                self.write(cr, uid, order.id, {'date_done':date})
        return res
    def set_done(self, cr, uid, ids, context=None):
        company_currency_id = self.pool.get('res.users').browse(cr, uid, uid, context).company_id.currency_id.id
        
        try:
            for order in self.browse(cr, uid, ids, context):
                date = order.date_done
#                if order.date_prefered == 'fixed':
#                    date = order.date_scheduled 
#                self.write(cr, uid, order.id, {'date_done':date})
                if order.create_account_moves != 'direct-payment':
                    continue
    
                for line in order.line_ids:
                    if not line.amount:
                        continue
                    
                    if line.payment_move_id:
                        continue
    
                    if not line.account_id:
                        raise osv.except_osv(_('Error!'), _('Payment order should create account moves but line with amount %.2f for partner "%s" has no account assigned.') % (line.amount, line.partner_id.name ) )
    
                    cr.rollback()
                    # This process creates a simple account move with bank and line accounts and line's amount. At the end
                    # it will reconcile or partial reconcile both entries if that is possible.
                    move_id = self.pool.get('account.move').create(cr, uid, {
                        'name': order.reference,
                        'ref': line.ml_inv_ref.number,
                        'journal_id': order.mode.journal.id,
                        'period_id': order.period_id.id,
                        'date':date,
                    }, context)
                    
                    currency_id = order.mode.journal.currency and order.mode.journal.currency.id or company_currency_id
    
                    if line.type == 'payable':
                        line_amount = line.amount_currency or line.amount
                    else:
                        line_amount = -line.amount_currency or -line.amount
                        
                    if line_amount >= 0:
                        account_id = order.mode.journal.default_credit_account_id.id
                    else:
                        account_id = order.mode.journal.default_debit_account_id.id
                    acc_cur = ((line_amount<=0) and order.mode.journal.default_debit_account_id) or line.account_id
    
                    ctx = context.copy()
                    ctx['res.currency.compute.account'] = acc_cur
                    amount = self.pool.get('res.currency').compute(cr, uid, currency_id, company_currency_id, line_amount, context=ctx)
    
                    val = {
                        'name': line.move_line_id and line.move_line_id.name or '/',
                        'move_id': move_id,
                        'date': date,
                        'ref': line.move_line_id and line.move_line_id.ref or False,
                        'partner_id': line.partner_id and line.partner_id.id or False,
                        'account_id': line.account_id.id,
                        'debit': ((amount>0) and amount) or 0.0,
                        'credit': ((amount<0) and -amount) or 0.0,
                        'journal_id': order.mode.journal.id,
                        'period_id': order.period_id.id,
                        'currency_id': currency_id,
                    }
                    
                    amount = self.pool.get('res.currency').compute(cr, uid, currency_id, company_currency_id, line_amount, context=ctx)
                    if currency_id <> company_currency_id:
                        amount_cur = self.pool.get('res.currency').compute(cr, uid, company_currency_id, currency_id, amount, context=ctx)
                        val['amount_currency'] = -amount_cur
    
                    if line.account_id and line.account_id.currency_id and line.account_id.currency_id.id <> company_currency_id:
                        val['currency_id'] = line.account_id.currency_id.id
                        if company_currency_id == line.account_id.currency_id.id:
                            amount_cur = line_amount
                        else:
                            amount_cur = self.pool.get('res.currency').compute(cr, uid, company_currency_id, line.account_id.currency_id.id, amount, context=ctx)
                        val['amount_currency'] = amount_cur
    
                    partner_line_id = self.pool.get('account.move.line').create(cr, uid, val, context, check=False)
    
                    # Fill the secondary amount/currency
                    # if currency is not the same than the company
                    if currency_id <> company_currency_id:
                        amount_currency = line_amount
                        move_currency_id = currency_id
                    else:
                        amount_currency = False
                        move_currency_id = False
    
                    self.pool.get('account.move.line').create(cr, uid, {
                        'name': line.move_line_id and line.move_line_id.name or '/',
                        'move_id': move_id,
                        'date': date,
                        'ref': line.move_line_id and line.move_line_id.ref or False,
                        'partner_id': line.partner_id and line.partner_id.id or False,
                        'account_id': account_id,
                        'debit': ((amount < 0) and -amount) or 0.0,
                        'credit': ((amount > 0) and amount) or 0.0,
                        'journal_id': order.mode.journal.id,
                        'period_id': order.period_id.id,
                        'amount_currency': amount_currency,
                        'currency_id': move_currency_id,
                    }, context)
    
                    move = self.pool.get('account.move').browse(cr, uid, move_id, context)
                    for x in move.line_id:
                        if x.state <> 'valid':
                            raise osv.except_osv(_('Error !'), _('Account move line "%s" is not valid') % x.name)
    
                    if line.move_line_id and not line.move_line_id.reconcile_id:
                        # If payment line has a related move line, we try to reconcile it with the move we just created.
                        lines_to_reconcile = [
                            partner_line_id,
                        ]
    
                        # Check if payment line move is already partially reconciled and use those moves in that case.
                        if line.move_line_id.reconcile_partial_id:
                            for rline in line.move_line_id.reconcile_partial_id.line_partial_ids:
                                lines_to_reconcile.append( rline.id )
                        else:
                            lines_to_reconcile.append( line.move_line_id.id )
    
                        amount = 0.0
                        for rline in self.pool.get('account.move.line').browse(cr, uid, lines_to_reconcile, context):
                            amount += rline.debit - rline.credit
    
                        currency = self.pool.get('res.users').browse(cr, uid, uid, context).company_id.currency_id
    
                        if self.pool.get('res.currency').is_zero(cr, uid, currency, amount):
                            self.pool.get('account.move.line').reconcile(cr, uid, lines_to_reconcile, 'payment', context=context)
                        else:
                            self.pool.get('account.move.line').reconcile_partial(cr, uid, lines_to_reconcile, 'payment', context)
    
                    if order.mode.journal.entry_posted:
                        self.pool.get('account.move').write(cr, uid, [move_id], {
                            'state':'posted',
                        }, context)
    
                    self.pool.get('payment.line').write(cr, uid, [line.id], {
                        'payment_move_id': move_id,
                    }, context)
                    cr.commit()
#            result = super(payment_order, self).set_done(cr, uid, ids, context)    
            wf_service = netsvc.LocalService("workflow")
            wf_service.trg_validate(uid, 'payment.order', ids[0], 'done', cr)
            result=True
        except Exception, e:
            cr.rollback()
            raise e
            return False
        
        return result
payment_order()