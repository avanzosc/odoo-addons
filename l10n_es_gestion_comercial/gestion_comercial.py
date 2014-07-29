# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2004-2012 Tiny SPRL (http://tiny.be). All Rights Reserved   
#
#    This module,
#    Copyright (C) 2011 Jose Ignacio Torrṕ - Soluntec(http://www.soluntec.es) 
#    Copyright (C) 2012 KM Sistemas de Información, S.L. - José Ignacio Torró
#    http://www.kmsistemas.com
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################


from osv import fields, osv
import netsvc
from tools import config
import account_check
import time
from tools.translate import _

#
# Diarios
#
#==================================================================================
#============================== INHERIT CLASS ACCOUNT JOURNAL======================
#==================================================================================
#Se modifica la clase de diarios contables para añadir nuevos campos que serán luego utilizados
#para determinar el comportamiento de los comprobantes de paggo

class account_journal(osv.osv):

# Se añaden a los comprobantes de pago, los campos de cheque recibido y de pago indirecto. 
# el campo de pago indirecto es un campo no visible, que se utilizará para registrar aquellos pagos que corresponden
# a documentos bancarios, es decir que no abonan directamente la factura sino que agrupan la deuda en un nuevo efecto cobrable

    _inherit = 'account.journal'
    _name = 'account.journal'
    _columns = {
         'indirect_payment': fields.boolean('Gestión de efectos comerciales', 
            help=("Marcar si se va a utilizar este diario para registrar "
            "apuntes de efectos correspondiente a gestión comercial (pagarés, "
            "giros, cheques, etc). El sistema usuará la cuenta definida en la "
            "ficha de cliente. Si está en blanco usuará la definida en este diario")),
         'without_account_efect': fields.boolean('Sin efecto contable', 
            help=("Si se marca esta opción, el sistema usará la cuenta de "
                  "cobrables/pagables del cliente en lugar de la cuenta de "
                  "fectos definidas en el diario o cliente")),                                                 
         'indirect_payment_type': fields.selection(
            [('documento','Documento de Cobro'),('impago','Impagos'),
            ('incobrable','Incobrable')],'Tipo de Efecto Comercial', 
            select=True),
	   
    }

account_journal()


#
# Partners
#
#==================================================================================
#============================== INHERIT CLASS RES_PARTNER==========================
#==================================================================================
#Se añade campos a los partners para registrar las cuentas a utilizar para efectos comerciales

class res_partner(osv.osv):

    _inherit = 'res.partner'
    _name = 'res.partner'
    
    
    _columns = {
        'property_account_efectos_cartera': fields.property(
            'account.account',
            type='many2one',
            relation='account.account',
            string="Efectos Comerciales en Cartera",
            method=True,
            view_load=True,
            domain="[('type', '=', 'receivable')]",
            help="Esta cuenta será utilizada en lugar de la cuenta por defecto del diario para registrar los efectos comerciales en cartera",
            required=False),
        'property_account_impagos': fields.property(
            'account.account',
            type='many2one',
            relation='account.account',
            string="Impagos",
            method=True,
            view_load=True,
            domain="[('type', '=', 'receivable')]",
            help="Esta cuenta será utilizada en lugar de la cuenta por defecto del diario para registrar los efectos impagados",
            required=False),
        'property_account_efectos_incobrables': fields.property(
            'account.account',
            type='many2one',
            relation='account.account',
            string="Incobrables",
            method=True,
            view_load=True,
            domain="[('type', '=', 'other')]",
            help="Esta cuenta será utilizada en lugar de la cuenta por defecto para registrar los efectos incobrables",
            required=False),
        'property_account_efectos_descontados': fields.property(
            'account.account',
            type='many2one',
            relation='account.account',
            string="Efectos Descontados",
            method=True,
            view_load=True,
            domain="[('type', '=', 'other')]",
            help="Cuenta para efectos descontados",
            required=False),
    }

res_partner()




#
# Comprobantes de Pago
#
#==================================================================================
#============================== INHERIT CLASS ACCOUNT VOUCHER======================
#==================================================================================
#Se modifica la gestión de comprobantes de pago para que amplie la funcionalidad para
#registrar pagos mediante pagarés,cheques, etc..

class account_voucher(osv.osv):

# Se añaden a los comprobantes de pago, los campos de cheque recibido y de pago indirecto. 
# el campo de pago indirecto es un campo no visible, que se utilizará para registrar aquellos pagos que corresponden
# a documentos bancarios, es decir que no abonan directamente la factura sino que agrupan la deuda en un nuevo efecto cobrable

    _inherit = 'account.voucher'
    _name = 'account.voucher'
    
    #================= METHODS =================#
    def onchange_partner_id(self, cr, uid, ids, partner_id, journal_id, price, currency_id, ttype, date, context=None):
            
        # We call the original event to give us back the original values
        res = super(account_voucher, self).onchange_partner_id(cr, uid, ids, partner_id, journal_id, price, currency_id, ttype, date)
        
        if journal_id:
            
            journal_pool = self.pool.get('account.journal')
            journal = journal_pool.browse(cr, uid, journal_id, context=context)
                    
          
            if journal.indirect_payment:
                res['value']['indirect_payment'] = True
            else:
                res['value']['indirect_payment'] = False    
        
        return res
    
    def action_move_line_create(self, cr, uid, ids, context=None):

        def _get_payment_term_lines(term_id, amount):
            term_pool = self.pool.get('account.payment.term')
            if term_id and amount:
                terms = term_pool.compute(cr, uid, term_id, amount)
                return terms
            return False
        if context is None:
            context = {}
        move_pool = self.pool.get('account.move')
        move_line_pool = self.pool.get('account.move.line')
        currency_pool = self.pool.get('res.currency')
        tax_obj = self.pool.get('account.tax')
        seq_obj = self.pool.get('ir.sequence')
        for inv in self.browse(cr, uid, ids, context=context):
            if inv.move_id:
                continue
            context_multi_currency = context.copy()
            context_multi_currency.update({'date': inv.date})

            if inv.number:
                name = inv.number
            elif inv.journal_id.sequence_id:
                name = seq_obj.get_id(cr, uid, inv.journal_id.sequence_id.id)
            else:
                raise osv.except_osv(_('Error !'), _('Please define a sequence on the journal !'))
            if not inv.reference:
                ref = name.replace('/','')
            else:
                ref = inv.reference

            move = {
                'name': name,
                'journal_id': inv.journal_id.id,
                'narration': inv.narration,
                'date': inv.date,
                'ref': ref,
                'period_id': inv.period_id and inv.period_id.id or False
            }
            move_id = move_pool.create(cr, uid, move)

            #create the first line manually
            company_currency = inv.journal_id.company_id.currency_id.id
            current_currency = inv.currency_id.id
            debit = 0.0
            credit = 0.0
            # TODO: is there any other alternative then the voucher type ??
            # -for sale, purchase we have but for the payment and receipt we do not have as based on the bank/cash journal we can not know its payment or receipt
            if inv.type in ('purchase', 'payment'):
                credit = currency_pool.compute(cr, uid, current_currency, company_currency, inv.amount, context=context_multi_currency)
            elif inv.type in ('sale', 'receipt'):
                debit = currency_pool.compute(cr, uid, current_currency, company_currency, inv.amount, context=context_multi_currency)
            if debit < 0:
                credit = -debit
                debit = 0.0
            if credit < 0:
                debit = -credit
                credit = 0.0
            sign = debit - credit < 0 and -1 or 1
            #create the first line of the voucher
            
            #Lineas modificadas respecto al original
            cuenta_id = False
            if inv.journal_id.indirect_payment:
                if inv.journal_id.without_account_efect:
                    cuenta_id = inv.partner_id.property_account_receivable.id,
                else:
                    if inv.journal_id.indirect_payment_type == "documento":
                        if inv.partner_id.property_account_efectos_cartera.id:
                            cuenta_id = inv.partner_id.property_account_efectos_cartera.id,
                        else:
                            cuenta_id = inv.account_id.id,
                    elif inv.journal_id.indirect_payment_type == "impago":
                        if inv.partner_id.property_account_impagos.id:
                            cuenta_id = inv.partner_id.property_account_impagos.id,
                        else:
                            cuenta_id = inv.account_id.id,
                    elif inv.journal_id.indirect_payment_type == "incobrable":
                        if inv.partner_id.property_account_efectos_incobrables.id:
                            cuenta_id = inv.partner_id.property_account_efectos_incobrables.id,
                        else:
                            cuenta_id = inv.account_id.id,                                
            else:
                cuenta_id = inv.account_id.id,
                          
            move_line = {
                'name': inv.name or '/',
                'debit': debit,
                'credit': credit,
                'account_id': cuenta_id[0],
                'move_id': move_id,
                'journal_id': inv.journal_id.id,
                'period_id': inv.period_id.id,
                'partner_id': inv.partner_id.id,
                'currency_id': company_currency <> current_currency and current_currency or company_currency,
                'amount_currency': company_currency <> current_currency and sign * inv.amount or 0.0,
                'date': inv.date,
                'date_maturity': inv.date_due
            }
            move_line_pool.create(cr, uid, move_line)
            rec_list_ids = []
            line_total = debit - credit
            if inv.type == 'sale':
                line_total = line_total - currency_pool.compute(cr, uid, inv.currency_id.id, company_currency, inv.tax_amount, context=context_multi_currency)
            elif inv.type == 'purchase':
                line_total = line_total + currency_pool.compute(cr, uid, inv.currency_id.id, company_currency, inv.tax_amount, context=context_multi_currency)

            for line in inv.line_ids:
                #create one move line per voucher line where amount is not 0.0
                if not line.amount:
                    continue
                #we check if the voucher line is fully paid or not and create a move line to balance the payment and initial invoice if needed
                if line.amount == line.amount_unreconciled:
                    amount = line.move_line_id.amount_residual #residual amount in company currency
                else:
                    amount = currency_pool.compute(cr, uid, current_currency, company_currency, line.untax_amount or line.amount, context=context_multi_currency)
                move_line = {
                    'journal_id': inv.journal_id.id,
                    'period_id': inv.period_id.id,
                    'name': line.name and line.name or '/',
                    'account_id': line.account_id.id,
                    'move_id': move_id,
                    'partner_id': inv.partner_id.id,
                    'currency_id': company_currency <> current_currency and current_currency or company_currency,
                    'analytic_account_id': line.account_analytic_id and line.account_analytic_id.id or False,
                    'quantity': 1,
                    'credit': 0.0,
                    'debit': 0.0,
                    'date': inv.date
                }
                if amount < 0:
                    amount = -amount
                    if line.type == 'dr':
                        line.type = 'cr'
                    else:
                        line.type = 'dr'

                if (line.type=='dr'):
                    line_total += amount
                    move_line['debit'] = amount
                else:
                    line_total -= amount
                    move_line['credit'] = amount

                if inv.tax_id and inv.type in ('sale', 'purchase'):
                    move_line.update({
                        'account_tax_id': inv.tax_id.id,
                    })
                if move_line.get('account_tax_id', False):
                    tax_data = tax_obj.browse(cr, uid, [move_line['account_tax_id']], context=context)[0]
                    if not (tax_data.base_code_id and tax_data.tax_code_id):
                        raise osv.except_osv(_('No Account Base Code and Account Tax Code!'),_("You have to configure account base code and account tax code on the '%s' tax!") % (tax_data.name))
                sign = (move_line['debit'] - move_line['credit']) < 0 and -1 or 1
                move_line['amount_currency'] = company_currency <> current_currency and sign * line.amount or 0.0
                voucher_line = move_line_pool.create(cr, uid, move_line)
                if line.move_line_id.id:
                    rec_ids = [voucher_line, line.move_line_id.id]
                    rec_list_ids.append(rec_ids)

            if not currency_pool.is_zero(cr, uid, inv.currency_id, line_total):
                diff = line_total
                account_id = False
                if inv.payment_option == 'with_writeoff':
                    account_id = inv.writeoff_acc_id.id
                elif inv.type in ('sale', 'receipt'):
                    account_id = inv.partner_id.property_account_receivable.id
                else:
                    account_id = inv.partner_id.property_account_payable.id
                move_line = {
                    'name': name,
                    'account_id': account_id,
                    'move_id': move_id,
                    'partner_id': inv.partner_id.id,
                    'date': inv.date,
                    'credit': diff > 0 and diff or 0.0,
                    'debit': diff < 0 and -diff or 0.0,
                    #'amount_currency': company_currency <> current_currency and currency_pool.compute(cr, uid, company_currency, current_currency, diff * -1, context=context_multi_currency) or 0.0,
                    #'currency_id': company_currency <> current_currency and current_currency or False,
                }
                move_line_pool.create(cr, uid, move_line)
            self.write(cr, uid, [inv.id], {
                'move_id': move_id,
                'state': 'posted',
                'number': name,
            })
            move_pool.post(cr, uid, [move_id], context={})
            for rec_ids in rec_list_ids:
                if len(rec_ids) >= 2:
                    move_line_pool.reconcile_partial(cr, uid, rec_ids)
        return True
       
    #================= FIELDS =================#
    _columns = {
         'payment_type': fields.many2one('payment.type', 'Tipo de Pago', help="Tipo de pago establecido para el nuevo efecto a crear"),
         'received_check': fields.boolean('Received check', help="To write down that a check in paper support has been received, for example.", invisible=True),
         'indirect_payment': fields.boolean('Document check', help="To mark if is not a direct payment"),
         'issued_check_ids':fields.one2many('account.issued.check', 'voucher_id', 'Cheques emitidos'),
         'third_check_receipt_ids':fields.one2many('account.third.check', 'voucher_id', 'Cheques de Terceros', required=False),
         'third_check_ids':fields.many2many('account.third.check', 'third_check_voucher_rel', 'third_check_id', 'voucher_id', 'Cheques de Terceros'),
         'property_account_gastos': fields.property(
             'account.account',
             type='many2one',
             relation='account.account',
             string="Cuenta Gastos",
             method=True,
             view_load=True,
             domain="[('type', '=', 'other')]",
             help="Gastos ocasionados por el impago",
             required=False), 
         'expense_amount': fields.float('Cantidad Gastos'),
         'invoice_expense':fields.boolean('Facturar Gastos?'),        

    }
    

account_voucher()


#
# Apuntes contables
#
#==================================================================================
#============================== INHERIT CLASS ACCOUNT VOUCHER======================
#==================================================================================
#Se realizan los siguientes cambios....
#Se sobreescribe el campo funcional de tipo de pago con una nueva versión que hace lo mismo pero buscando ademas 
#el valor del comprante de pago si el efecto no esta relacionado directamente con una factura

class account_move_line(osv.osv):
    _name = 'account.move.line'
    _inherit = 'account.move.line'

# Se amplia el metodo original de account_payment_extension. Ahora si no encuentra el tipo de pago en la factura 
# asociada el apunte, lo busca en el comprobante de pago... Si no esta en ninguno de los dos, lo deja en blanco.  
    def _payment_type_get(self, cr, uid, ids, field_name, arg, context=None):
        result = {}
        invoice_obj = self.pool.get('account.invoice')
        voucher_obj = self.pool.get('account.voucher')
        for move_line in self.browse(cr, uid, ids, context=context):
            result[move_line.id] = False
            invoice_ids = invoice_obj.search(cr, uid, 
                    [('move_id', '=', move_line.move_id.id)], context=context)
            if invoice_ids:
                inv = invoice_obj.browse(cr, uid, invoice_ids[0],
                    context=context)
                if inv.payment_type:
                    result[move_line.id] = inv.payment_type.id
            else:
                voucher_ids = voucher_obj.search(cr, uid, 
                    [('move_id', '=', move_line.move_id.id)], context=context)
                if voucher_ids:
                    voucher = voucher_obj.browse(cr, uid, voucher_ids[0], 
                        context=context)
                    if voucher.payment_type:
                        result[move_line.id] = voucher.payment_type.id
        return result

#Sin modificaciones del original de momento... hay que hacer que encuentre los heredados del comprobante de cobro
    def _payment_type_search(self, cr, uid, obj, name, args, context=None):
        if not len(args):
            return []
#        operator = args[0][1]
        value = args[0][2]
        if not value:
            return []
        if isinstance(value, int) or isinstance(value, long):
            ids = [value]
        elif isinstance(value, list):
            ids = value 
        else:
            ids = self.pool.get('payment.type').search(cr,uid,[('name','ilike',value)], context=context)
        if ids:
            cr.execute('SELECT l.id ' \
                'FROM account_move_line l, account_invoice i, account_voucher j ' \
                'WHERE (l.move_id = j.move_id AND j.payment_type = ' + str(ids[0]) + ') OR (l.move_id = i.move_id AND i.payment_type in (%s))' % (','.join(map(str, ids))))
            res = cr.fetchall()
            if len(res):
                return [('id', 'in', [x[0] for x in res])]
        return [('id','=','0')]
 
## Se crea un nuevo campo funcional de tipo booleano que obtiene si es pago corresponde a un efecto de gestión comercial o no.    
    def _indirect_payment_get(self, cr, uid, ids, field_name, arg, context=None):
        result = {}
        voucher_obj = self.pool.get('account.voucher')
        for move_line in self.browse(cr, uid, ids, context=context):
            result[move_line.id] = False
            voucher_ids = voucher_obj.search(cr, uid, 
                [('move_id', '=', move_line.move_id.id)], context=context)
            if voucher_ids:
                voucher = voucher_obj.browse(cr, uid, voucher_ids[0], 
                        context=context)
                if voucher.indirect_payment:
                    if move_line.debit > 0: #move_line.id.account_id.type = 'receivable'
                        result[move_line.id] = True              
        return result
 
# Creamos los metodos de busqueda para obtener los registros que tienen el check de efecto de gestión comercial marcado   
    def _indirect_payment_search(self, cr, uid, obj, name, args, context={}):
        """ Definition for searching account move lines with indirect_payment check ('indirect_payment','=',True)"""
        for x in args:
            if (x[2] is True) and (x[1] == '=') and (x[0] == 'indirect_payment'):
                cr.execute('SELECT l.id FROM account_move_line l ' \
                    'LEFT JOIN account_voucher i ON l.move_id = i.move_id ' \
                    'WHERE i.indirect_payment = TRUE AND l.debit > 0', []) # NOTA A MEJORAR CUANDO DEBAN INCLUIRSE LOS EFECTOS DE PAGO
                res = cr.fetchall()
                if not len(res):
                    return [('id', '=', '0')]
            elif (x[2] is False) and (x[1] == '=') and (x[0] == 'indirect_payment'):
                cr.execute('SELECT l.id FROM account_move_line l ' \
                    'LEFT JOIN account_voucher i ON l.move_id = i.move_id ' \
                    'WHERE i.indirect_payment = FALSE', []) 
                res = cr.fetchall()
                if not len(res):
                    return [('id', '=', '0')]
        return [('id', 'in', [x[0] for x in res])]
        
    def _get_move_lines_invoice(self, cr, uid, ids, context=None):
        result = set()
        invoice_obj = self.pool.get('account.invoice')
        for invoice in invoice_obj.search(cr, uid, ids, context=context):
            if invoice.move_id:
                for move_line in invoice.move_id.line_id:
                    result.add(move_line.id)
        return result
    
    def _get_move_lines_voucher(self, cr, uid, ids, context=None):
        result = set()
        invoice_obj = self.pool.get('account.voucher')
        for invoice in invoice_obj.search(cr, uid, ids, context=context):
            if invoice.move_id:
                for move_line in invoice.move_id.line_id:
                    result.add(move_line.id)
        return result
    
    _columns = {
         'payment_type': fields.function(_payment_type_get, 
                fnct_search=_payment_type_search, method=True, type="many2one", 
                relation="payment.type", string="Payment type",
                store={
                       'account.move.line':(lambda self, cr, uid, ids,
                                context=None: ids, None, 20),
                       'account.invoice':(_get_move_lines_invoice, ['move_id'],
                                          20),
                       'account.voucher':(_get_move_lines_voucher, ['move_id'],
                                          20),
                }),
         'indirect_payment': fields.function(_indirect_payment_get, 
                fnct_search=_indirect_payment_search, method=True, 
                type="boolean", string="Indirect Payment",
                store={
                       'account.move.line':(lambda self, cr, uid, ids,
                                context=None: ids, None, 20),
                       'account.voucher':(_get_move_lines_voucher, ['move_id'], 
                                          20),
                       }),
         'payment_order_check': fields.boolean("Mostrar en Efectos"),
         'to_concile_account': fields.many2one('account.account', 
                'Expected Account To Concile', required=False, 
                help=('Cuenta con la que deberá ser concilada en un '
                'apunte posterior')),


    }
account_move_line()


#
# Modo de Pago
#
#==================================================================================
#============================== INHERIT CLASS PAYMENT_MODE=========================
#==================================================================================
#Se añaden campos a los modos de pago para poder gestionar los descuentos de efectos

class payment_mode(osv.osv):
    _inherit = 'payment.mode'
    _columns = {
        'cuenta_deuda_efectos_descontados': fields.many2one('account.account', 'Cuenta Deuda Efectos Descontados', required=False, help='Cuenta para efectos descontados. Ejemplo: 5208xx'),
        'cuenta_factoring': fields.many2one('account.account', 'Cuenta Deudas por Operaciones de Factoring', required=False, help='Cuenta para deudas por operaciones de Factoring. Ejemplo: 5209xx'),
        'cuenta_efectos_descontados': fields.many2one('account.account', 'Cuenta Genérica Efectos Descontados', required=False, help='Cuenta para efectos descontados. Ejemplo: 4311x'),
      }
    _defaults = {
        'cuenta_deuda_efectos_descontados': lambda *a: '705',
        'cuenta_factoring': lambda *a: '707',
        'cuenta_efectos_descontados': lambda *a: '528',
    }
payment_mode()


#
# Orden de Cobro
#
#==================================================================================
#============================== INHERIT CLASS PAYMENT_ORDER========================
#==================================================================================
#Se amplia la funcuonalidad de las ordenes de cobro para registrar descuentos de efectos

class payment_order(osv.osv):
    _name = 'payment.order'
    _inherit = 'payment.order'

    _columns = {
        'create_account_moves': fields.selection([('bank-statement','Bank Statement'),('direct-payment','Direct Payment'),('factoring','Factoring'),('descuento-efecto','Descuento de Efectos')],
                                                 'Create Account Moves',
                                                 required=True,
                                                 states={'done':[('readonly',True)]},
                                                 help='Indicates when account moves should be created for order payment lines. "Bank Statement" '\
                                                      'will wait until user introduces those payments in bank a bank statement. "Direct Payment" '\
                                                      'will mark all payment lines as payied once the order is done.'),
        'expense_moves':fields.boolean('Contabilizar Gastos?'),
        'value_amount': fields.float('% Interés', help="% de gastos sobre cobro"),
        'expense_account': fields.many2one('account.account', 'Cuenta Gastos', required=False, help='Cuenta para gastos de cobro'),
        'due_date': fields.date('Fecha Vencimiento'),
    }

    def set_done(self, cr, uid, ids, context=None):
        result = super(payment_order, self).set_done(cr, uid, ids, context)
        company_currency_id = self.pool.get('res.users').browse(cr, uid, uid, context).company_id.currency_id.id

        for order in self.browse(cr, uid, ids, context):
            if ((order.create_account_moves != 'direct-payment') and (order.create_account_moves != 'factoring') and (order.create_account_moves != 'descuento-efecto')):
                continue
            
            move_id = self.pool.get('account.move').create(cr, uid, {
                'name': '/',
                'journal_id': order.mode.journal.id,
                'period_id': order.period_id.id,
            }, context)

            partner_line_id = {}
            ref = ""
            
            for line in order.line_ids:
                if not line.amount:
                    continue

                if not line.account_id:
                    raise osv.except_osv(_('Error!'), _('Payment order should create account moves but line with amount %(amount).2f for partner "%(partner)s" has no account assigned.') % {'amount': line.amount, 'partner': line.partner_id.name} )

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
                    'date': order.date_done,
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

                partner_line_id[line.move_line_id] = self.pool.get('account.move.line').create(cr, uid, val, context, check=False)

                ## Creamos el apunte de descuento de efectos o factoring
                if ((order.create_account_moves == 'factoring') or (order.create_account_moves == 'descuento-efecto')):
                    if (order.create_account_moves == 'descuento-efecto'):
                        cuenta_deuda_descuento_efectos = order.mode.cuenta_deuda_efectos_descontados.id
                    if (order.create_account_moves == 'factoring'):
                        cuenta_deuda_descuento_efectos = order.mode.cuenta_factoring.id
                    
                    val_ef_descontados = {
                           'name': line.move_line_id and line.move_line_id.name or '/',
                           'move_id': move_id,
                           'date': order.date_done,
                           'ref': line.move_line_id and line.move_line_id.ref or False,
                           'partner_id': line.partner_id and line.partner_id.id or False,
                           'account_id': cuenta_deuda_descuento_efectos,
                           'debit': ((amount>0) and amount) or 0.0,
                           'credit': ((amount<0) and -amount) or 0.0,
                           'journal_id': order.mode.journal.id,
                           'period_id': order.period_id.id,
                           'currency_id': currency_id,
                    }
                    
                    partner_line_id_efectos_descontados = self.pool.get('account.move.line').create(cr, uid, val_ef_descontados, context, check=False)
                    


                # Fill the secondary amount/currency
                # if currency is not the same than the company
                if currency_id <> company_currency_id:
                    amount_currency = line_amount
                    move_currency_id = currency_id
                else:
                    amount_currency = False
                    move_currency_id = False
 
                
                if order.expense_moves:
                    self.pool.get('account.move.line').create(cr, uid, {
                        'name': line.move_line_id and line.move_line_id.name or '/',
                        'move_id': move_id,
                        'date': order.date_done,
                        'ref': line.move_line_id and line.move_line_id.ref or False,
                        'partner_id': line.partner_id and line.partner_id.id or False,
                        'account_id': account_id,
                        'debit': ((amount < 0) and -(amount-(amount*(order.value_amount/100)))) or 0.0,
                        'credit': ((amount > 0) and (amount-(amount*(order.value_amount/100)))) or 0.0,
                        'journal_id': order.mode.journal.id,
                        'period_id': order.period_id.id,
                        'amount_currency': (amount_currency-(amount_currency*(order.value_amount/100))),
                        'currency_id': move_currency_id,
                    }, context, check = False)
                    
                    self.pool.get('account.move.line').create(cr, uid, {
                        'name': line.move_line_id and line.move_line_id.name or '/',
                        'move_id': move_id,
                        'date': order.date_done,
                        'ref': line.move_line_id and line.move_line_id.ref or False,
                        'partner_id': line.partner_id and line.partner_id.id or False,
                        'account_id': order.expense_account.id,
                        'debit': ((amount < 0) and -((amount*(order.value_amount/100)))) or 0.0,
                        'credit': ((amount > 0) and ((amount*(order.value_amount/100)))) or 0.0,
                        'journal_id': order.mode.journal.id,
                        'period_id': order.period_id.id,
                        'amount_currency': ((amount_currency*(order.value_amount/100))),
                        'currency_id': move_currency_id,
                    }, context, check = False)
                else:
                    self.pool.get('account.move.line').create(cr, uid, {
                        'name': line.move_line_id and line.move_line_id.name or '/',
                        'move_id': move_id,
                        'date': order.date_done,
                        'ref': line.move_line_id and line.move_line_id.ref or False,
                        'partner_id': line.partner_id and line.partner_id.id or False,
                        'account_id': account_id,
                        'debit': ((amount < 0) and -amount) or 0.0,
                        'credit': ((amount > 0) and amount) or 0.0,
                        'journal_id': order.mode.journal.id,
                        'period_id': order.period_id.id,
                        'amount_currency': amount_currency,
                        'currency_id': move_currency_id,
                    }, context, check = False)

                ## Creamos el apunte de descuento de efectos
                ref = ""
                
                if ((order.create_account_moves == 'factoring') or (order.create_account_moves == 'descuento-efecto')):
                    
                    #Si el cliente tiene informada la cuenta de efectos descontados usamos esa.. si no usamos la del modo de pago
                    if line.partner_id.property_account_efectos_descontados:
                        cuenta_descuento_efectos = line.partner_id.property_account_efectos_descontados.id,
                        
                    else:
                        cuenta_descuento_efectos = order.mode.cuenta_efectos_descontados.id,
                    
                                    
                    self.pool.get('account.move.line').create(cr, uid, {
                        'name': line.move_line_id and line.move_line_id.name or '/',
                        'move_id': move_id,
                        'date': order.date_done,
                        'ref': line.move_line_id and line.move_line_id.ref or False,
                        'partner_id': line.partner_id and line.partner_id.id or False,
                        'account_id': cuenta_descuento_efectos[0],
                        'debit': ((amount < 0) and -amount) or 0.0,
                        'credit': ((amount > 0) and amount) or 0.0,
                        'journal_id': order.mode.journal.id,
                        'period_id': order.period_id.id,
                        'amount_currency': amount_currency,
                        'currency_id': move_currency_id,
                        #'date_maturity': order.due_date, :# LINEA ORIGINAL
                        'date_maturity': order.due_date or line.date or line.move_line_id.date_maturity,
                        'payment_order_check': True,
                        'to_concile_account': cuenta_deuda_descuento_efectos,
                    }, context, check = False)
                    
                   
                    if order.create_account_moves == 'factoring':
                        ref = unicode('Factoring /') + order.mode.journal.name
                    if order.create_account_moves == 'descuento-efecto':
                        ref = unicode('Desc. de efectos /') + order.mode.journal.name
                    
                    
            #>> KMS: sacamos la conciliación/validación de los efectos fuera del bucle de las líneas, para que no dé error de asiento ya reconciliado
            #                 ya que cuando intenta validar el asiento por cada efecto, comprueba todas las líneas (se genera un único asiento de toda la remesa)
            # (-) VALIDACIÓN
            self.pool.get('account.move').validate(cr, uid, [move_id], context=context)
            aml_ids = [x.id for x in self.pool.get('account.move').browse(cr, uid, move_id, context).line_id]
            for x in self.pool.get('account.move.line').browse(cr, uid, aml_ids, context):
                if x.state <> 'valid':
                    raise osv.except_osv(_('Error !'), _('Account move line "%s" is not valid') % x.name)
                self.pool.get('account.move.line').write(cr, uid, [x.id], {'ref':ref}, context=None, check=False)

            # (-) CONCILIACIÓN
            for line in order.line_ids:
                if line.move_line_id and not line.move_line_id.reconcile_id:
                    # If payment line has a related move line, we try to reconcile it with the move we just created.
                    lines_to_reconcile = [
                        partner_line_id[line.move_line_id],
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

            #<<< KMS           

            if order.mode.journal.entry_posted:
                self.pool.get('account.move').write(cr, uid, [move_id], {
                    'state':'posted',
                }, context)

            self.pool.get('payment.line').write(cr, uid, [line.id], {
                'payment_move_id': move_id,
            }, context)

        return result

payment_order()
