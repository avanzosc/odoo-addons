# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc - Advanced Open Source Consulting
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
from mx import DateTime

import netsvc
from osv import osv
from osv import fields
from tools.translate import _

class sale_order(osv.osv):
    _name = 'sale.order'
    _inherit = 'sale.order'
    
    _columns = {
                'visa_pay':fields.boolean('Visa Payment'),
                }
    def create_invoice_payment(self, cr, uid, invoice_id, context={}):
        invoice_obj = self.pool.get('account.invoice')
        move_pool = self.pool.get('account.move')
        move_line_pool = self.pool.get('account.move.line')
        journal_pool = self.pool.get('account.journal')
        seq_obj = self.pool.get('ir.sequence')
        currency_pool = self.pool.get('res.currency')
        
        inv = invoice_obj.browse(cr,uid,invoice_id)
        invoice_move = inv.move_id
        move_line_name = invoice_move.name
        reconcile = []
        
        inv_line_list = move_line_pool.search(cr,uid,[('move_id', '=', invoice_move.id), ('account_id', '=', inv.account_id.id)])
        if inv_line_list:
            reconcile.append(inv_line_list[0])
        context_multi_currency = context.copy()
        context_multi_currency.update({'date': inv.date_invoice})
        
        #=======================================================================
        # METEMOS EL ID DEL DIARIO DIRECTAMENTE
        # Diario a utilizar para pagos en visa en este caso concreto
        # B19 CATALUNYA CAIXA VISA = 96
        #=======================================================================
        journal_id = 96
#        journal_id = 95
        journal_o =journal_pool.browse(cr, uid, journal_id) 
        
        #=======================================================================
        # ASIENTO CONTABLE
        #=======================================================================
        
        if journal_o.sequence_id:
            name = seq_obj.get_id(cr, uid, journal_o.sequence_id.id)
        if not name:
            raise osv.except_osv(_('Error !'), _('Please define a sequence on the journal and make sure it is activated !'))
        
        ref = 'VISA - ' + name.replace('/','')
        
        move = {
                'name': name,
                'journal_id': journal_id,
#                'narration': narration,
                'date': inv.date_invoice,
                'ref': ref,
                'period_id': inv.period_id and inv.period_id.id or False
            }
        move_id = move_pool.create(cr, uid, move)
        
        #===============================================================================
        # LINEA CORRESPONDIENTE AL PAGO
        #===============================================================================
        company_currency = journal_o.company_id.currency_id.id
        current_currency = inv.currency_id.id
        debit = 0.0
        credit = 0.0
        
        debit = currency_pool.compute(cr, uid, current_currency, company_currency, inv.amount_total, context=context_multi_currency)
        if debit < 0:
            credit = -debit
            debit = 0.0
        if credit < 0:
            debit = -credit
            credit = 0.0
        sign = debit - credit < 0 and -1 or 1
        
        move_line = {
                'name': move_line_name,
                'debit': debit,
                'credit': credit,
                'account_id': journal_o.default_debit_account_id.id,
                'move_id': move_id,
                'journal_id': journal_id,
                'period_id': inv.period_id.id,
                'partner_id': inv.partner_id.id,
                'currency_id': company_currency <> current_currency and  current_currency or False,
                'amount_currency': company_currency <> current_currency and sign * inv.amount_total or 0.0,
                'date': inv.date_invoice,
                'date_maturity': inv.date_invoice
            }
        move_line_pool.create(cr, uid, move_line)
        
        #===============================================================================
        # LINEA CORRESPONDIENTE AL CLIENTE
        #===============================================================================      
        
        move_line = {
                    'journal_id': journal_id,
                    'period_id': inv.period_id.id,
                    'name': move_line_name,
                    'account_id': inv.account_id.id,
                    'move_id': move_id,
                    'partner_id': inv.partner_id.id,
                    'currency_id': company_currency <> current_currency and current_currency or False,
#                    'analytic_account_id': line.account_analytic_id and line.account_analytic_id.id or False,
                    'quantity': 1,
                    'credit': debit,
                    'debit': credit,
                    'date': inv.date_invoice
                }
        
        pay_line_id = move_line_pool.create(cr, uid, move_line)
        reconcile.append(pay_line_id)
        
        move_pool.post(cr, uid, [move_id], context={})
        if len(reconcile) >= 2:
            move_line_pool.reconcile_partial(cr, uid, reconcile)
        return inv
    
    
    
    def create_visa_invoice(self, cr, uid, ids, context={}):
        
        invoice_obj = self.pool.get('account.invoice')
        obj_sale_order_line = self.pool.get('sale.order.line')
        payment_type_pool = self.pool.get('payment.type')
        journal_obj = self.pool.get('account.journal')
        
        inv=False
        lines=[]
        
        for order in self.browse(cr, uid, ids, context):
            #===================================================================
            # AÑADIMOS EL ID DEL TIPO DE PAGO  DIRECTAMENTE
            # tarjeta = 4 -- en este caso especifico
            #===================================================================
            pay_type =  4
            #=======================================================================================
            # CREAMOS LA LÍNEAS DE FACTURA PARA TODAS LAS LÍNEAS DE PEDIDO QUE SON PAGABLES EN VISA
            #=======================================================================================       
            for line in order.order_line:
                if line.visa_pay:
                    lines.append(line.id)
            line_list = obj_sale_order_line.invoice_line_create(cr, uid, lines)
            #===================================================================
            # BUSCAR EL DIARIO DE VENTA MÁS RECIENTE
            #===================================================================
            journal_list = journal_obj.search(cr,uid,[('name', 'like', 'Sales Journal'),('type','=', 'sale')])
            journal_list.reverse()
            journal_id = journal_list[0]
            
            #===================================================================
            # CREAMOS LA FACTURA PARA EL PEDIDO Y LE CARGAMOS EL TIPO DE PAGO
            #===================================================================
            inv = self._make_invoice(cr, uid, order, line_list, context=context)
            invoice_obj.write(cr,uid,[inv],{'payment_type':pay_type, 'visa_pay':True, 'journal_id':journal_id})
            
            #===================================================================
            # CONFIRMAMOS LA FACTURA
            #===================================================================
            wf_service = netsvc.LocalService("workflow")
            wf_service.trg_validate(uid, 'account.invoice', inv, 'invoice_open', cr)
            
            #===================================================================
            # ENLAZAMOS LA FACTURA CON EL PEDIDO DE VENTA
            #===================================================================
            cr.execute('insert into sale_order_invoice_rel (order_id,invoice_id) values (%s,%s)', (order.id, inv))
            
            #===================================================================
            # CREAMOS EL PAGO Y LO CONCILIAMOS CON LA FACTURA
            #===================================================================
            self.create_invoice_payment(cr, uid, inv, context)
        return inv
    
    #===========================================================================
    # FUNCIÓN COPIA DE avanzosc_agreement_fixed_price
    #===========================================================================
    def action_create_analytic_lines(self, cr, uid, ids, context=None):
        res = False
        values = {}
        obj_sale_order_line = self.pool.get('sale.order.line')
        obj_account_analytic_line = self.pool.get('account.analytic.line')
        obj_factor = self.pool.get('hr_timesheet_invoice.factor')
        obj_agreement = self.pool.get('inv.agreement')
        if context is None:
            context = {}
        for order in self.browse(cr, uid, ids, context=context):
            analytic_account = order.project_id.id
            factor = obj_factor.search(cr, uid, [('factor', '=', 0)])[0]
            #===================================================================
            # CREAR FACTURA MANUALMENTE SI EL PEDIDO ES PAGADO EN VISA
            #===================================================================
            if order.visa_pay:
                self.create_visa_invoice(cr,uid,[order.id], context)
            for line in order.order_line:
                #===============================================================
                # NO CREAR ANALÍTICA PARA LAS LÍNEAS PAGABLES EN VISA
                #===============================================================
                if not line.analytic_created and not line.visa_pay:
                    if line.product_id.property_account_income:
                        general_account = line.product_id.property_account_income.id
                    else:
                        general_account = line.product_id.categ_id.property_account_income_categ.id
                    if not line.invoice_date:
                        raise osv.except_osv(_('User error'), _('Invoice Date not found for: %s') %(line.product_id.name))
                    values = {
                            'date': line.invoice_date,
                            'account_id': analytic_account,
                            'unit_amount': line.product_uom_qty,
                            'name': line.name,
                            'sale_amount':line.price_subtotal,
                            'general_account_id': general_account,
                            'product_id': line.product_id.id,
                            'product_uom_id': line.product_id.uom_id.id,
                            'ref': order.name,
                            'to_invoice': factor,
                            'journal_id': 1,
                            'sale_id': order.id,
                        }
                    if line.invoice_mode == 'once':   
                        values.update({
                            'sale_amount': line.price_unit,
                        })
                        obj_account_analytic_line.create(cr,uid,values)
                    elif line.invoice_mode == 'installments':
                        amount = line.price_subtotal / line.installments
                        values.update({
                            'sale_amount': amount,
                        })
                        if line.installment_unit == 'days':
                            increment_size = DateTime.RelativeDateTime(days=1)
                        elif line.installment_unit == 'weeks':
                            increment_size = DateTime.RelativeDateTime(days=7)
                        elif line.installment_unit == 'months':
                            increment_size = DateTime.RelativeDateTime(months=1)
                        elif line.installment_unit == 'years':
                            increment_size = DateTime.RelativeDateTime(months=12)
                        cont = line.installments
                        while cont > 0:
                            obj_account_analytic_line.create(cr,uid,values)
                            next_date = DateTime.strptime(values['date'], '%Y-%m-%d') + increment_size
                            values.update({
                                'date': next_date.strftime('%Y-%m-%d'),
                            })
                            cont-=1
                    elif line.invoice_mode in ('recur', 'recur_install'):
                        values = {
                            'partner_id': order.partner_id.id,
                            'service': line.product_id.recur_service.id,
                            'signed_date': line.invoice_date,
                            'cur_effect_date': line.expire_date,
                            'partner_signed_date': line.partner_signed_date or line.invoice_date,
                            'analytic_account': analytic_account,
                            'payment': line.payment,
                            'recurr_unit_number': line.interval,
                            'recurr_unit': line.interval_unit,
                            'period_unit_number': line.period,
                            'period_unit': line.period_unit,
                            #'fixed_price': line.price_subtotal,
                            'fixed_price': line.price_unit,
                            'sale_order_line':line.id,
                        }
                        if line.invoice_mode == 'recur_install':
                            values.update({'fixed_price':line.price_unit, 'fixed_price_extra':line.amount_month, 'period_qty':line.month_qty})
                        id = obj_agreement.create(cr, uid, values)
                        self.write(cr, uid, [order.id], {'agreement': id})
                        obj_agreement.get_number(cr, uid, [id])
                        obj_agreement.set_process(cr, uid, [id]) 
                       
        return res
sale_order()

class sale_order_line(osv.osv):
    _name = 'sale.order.line'
    _inherit = 'sale.order.line'
    
    def _calc_is_visa(self, cr, uid, ids, field_name, arg, context={}):
        res = {}
        for id in ids:
            val = False
            line_o = self.browse(cr,uid,id)
            if line_o.product_id and line_o.order_id:
                if line_o.product_id.visa_pay and line_o.order_id.visa_pay:
                    val = True
            res[id] = val
        return res
    
    _columns = {
                'visa_pay':fields.function(_calc_is_visa, method=True, type="boolean", string="Visa Payable", readonly=True)
                }
sale_order_line()