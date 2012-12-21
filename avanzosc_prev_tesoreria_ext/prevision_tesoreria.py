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
import decimal_precision as dp
import base64
import unicodedata
import math
from osv import osv
from osv import fields
import tools



class l10n_es_tesoreria_facturas(osv.osv):
    _name = 'l10n.es.tesoreria.facturas'
    _inherit = 'l10n.es.tesoreria.facturas'
    _columns = {
              'inv_type':fields.related('factura_id', 'type', type="selection", selection=[('out_invoice', 'Customer Invoice'),
            ('in_invoice', 'Supplier Invoice'),
            ('out_refund', 'Customer Refund'),
            ('in_refund', 'Supplier Refund'), ], string="Tipo"),
              'payment_term':fields.many2one('account.payment.term', 'Plazo de Pago'),
              }
l10n_es_tesoreria_facturas()

class l10n_es_tesoreria(osv.osv):
    _name = 'l10n.es.tesoreria'
    _inherit = 'l10n.es.tesoreria'
    

    def _calcular_saldo(self, cr, uid, ids, name, args, context=None):
        res = {}
        saldo = 0
        for teso in self.browse(cr, uid, ids):
            for fact_emit in teso.facturas_emit:
                saldo += fact_emit.total
            for fact_rec in teso.facturas_rec:
                saldo -= fact_rec.total
            for pagoP in teso.pagos_period:
                saldo -= pagoP.importe
            for pagoV in teso.pagos_var:
                saldo -= pagoV.importe
            for pagoR in teso.pagos_rece:
                saldo += pagoR.importe
            for pagoC in teso.pagos_cash:
                saldo += pagoC.importe
            saldo += teso.saldo_inicial
            res[teso.id] = saldo
        return res
    
    _columns = {
                'pagos_rece':fields.one2many('l10n.es.tesoreria.pagos.rece', 'tesoreria_id', 'Cobros Unicos'),
                'pagos_cash':fields.one2many('l10n.es.tesoreria.pagos.cash', 'tesoreria_id', 'Cash-flow Financiero'),
                'saldo_final': fields.function(_calcular_saldo, method=True, digits_compute=dp.get_precision('Account'), string='Saldo Final'),
                }
    def button_saldo(self, cr, uid, ids, context=None):
        res = {}
        saldo = 0
        saldos_obj = self.pool.get('l10n.es.tesoreria.saldos')
        for teso in self.browse(cr, uid, ids):
            for saldo in teso.desglose_saldo:
                saldos_obj.unlink(cr, uid, saldo.id)
            for fact_emit in teso.facturas_emit:
                if fact_emit.tipo_pago:
                    name = fact_emit.tipo_pago.name
                else:
                    name = 'Undefined'
                if fact_emit.inv_type == 'out_invoice':
                    saldo_id = saldos_obj.search(cr, uid, [('name', '=', name), ('tesoreria_id', '=', teso.id), ('type', '=', 'in')])
                    if saldo_id:
                        saldo = saldos_obj.browse(cr, uid, saldo_id[0])
                        saldos_obj.write(cr, uid, saldo.id, {'saldo': saldo.saldo + math.fabs(fact_emit.total)})
                    else:
                        saldos_obj.create(cr, uid, {'name': name, 'saldo': math.fabs(fact_emit.total), 'tesoreria_id': teso.id, 'type':'in'})
                    
                if fact_emit.inv_type == 'out_refund':
                    saldo_id = saldos_obj.search(cr, uid, [('name', '=', name), ('tesoreria_id', '=', teso.id), ('type', '=', 'out')])
                    if saldo_id:
                        saldo = saldos_obj.browse(cr, uid, saldo_id[0])
                        saldos_obj.write(cr, uid, saldo.id, {'saldo': saldo.saldo + math.fabs(fact_emit.total)})
                    else:
                        saldos_obj.create(cr, uid, {'name': name, 'saldo': math.fabs(fact_emit.total), 'tesoreria_id': teso.id, 'type':'out'})
            for fact_rec in teso.facturas_rec:
                if fact_emit.tipo_pago:
                    name = fact_emit.tipo_pago.name
                else:
                    name = 'Undefined'
                if fact_rec.inv_type == 'in_invoice':
                    saldo_id = saldos_obj.search(cr, uid, [('name', '=', name), ('tesoreria_id', '=', teso.id), ('type', '=', 'out')])
                    if saldo_id:
                        saldo = saldos_obj.browse(cr, uid, saldo_id[0])
                        saldos_obj.write(cr, uid, saldo.id, {'saldo': saldo.saldo + math.fabs(fact_rec.total)})
                    else:
                        saldos_obj.create(cr, uid, {'name': name, 'saldo': math.fabs(fact_rec.total), 'tesoreria_id': teso.id, 'type':'out'})
                if fact_rec.inv_type == 'in_refund':
                    saldo_id = saldos_obj.search(cr, uid, [('name', '=', name), ('tesoreria_id', '=', teso.id), ('type', '=', 'in')])
                    if saldo_id:
                        saldo = saldos_obj.browse(cr, uid, saldo_id[0])
                        saldos_obj.write(cr, uid, saldo.id, {'saldo': saldo.saldo + math.fabs(fact_rec.total)})
                    else:
                        saldos_obj.create(cr, uid, {'name': name, 'saldo': math.fabs(fact_rec.total), 'tesoreria_id': teso.id, 'type':'in'})
            for pagoV in teso.pagos_var:
                if pagoV.payment_type:
                    name = pagoV.payment_type.name
                else:
                    name = 'Undefined'
                saldo_id = saldos_obj.search(cr, uid, [('name', '=', name), ('tesoreria_id', '=', teso.id), ('type', '=', 'out')])
                if saldo_id:
                    saldo = saldos_obj.browse(cr, uid, saldo_id[0])
                    saldos_obj.write(cr, uid, saldo.id, {'saldo': saldo.saldo + math.fabs(pagoV.importe)})
                else:
                    saldos_obj.create(cr, uid, {'name': name, 'saldo': math.fabs(pagoV.importe), 'tesoreria_id': teso.id, 'type':'out'})
            for pagoP in teso.pagos_period:
                if pagoP.payment_type:
                    name = pagoP.payment_type.name
                else:
                    name = 'Undefined'
                saldo_id = saldos_obj.search(cr, uid, [('name', '=', name), ('tesoreria_id', '=', teso.id), ('type', '=', 'out')])
                if saldo_id:
                    saldo = saldos_obj.browse(cr, uid, saldo_id[0])
                    saldos_obj.write(cr, uid, saldo.id, {'saldo': saldo.saldo + math.fabs(pagoP.importe)})
                else:
                    saldos_obj.create(cr, uid, {'name': name, 'saldo': math.fabs(pagoP.importe), 'tesoreria_id': teso.id, 'type':'out'})
            for pagoR in teso.pagos_rece:
                if pagoR.payment_type:
                    name = pagoR.payment_type.name
                else:
                    name = 'Undefined'
                saldo_id = saldos_obj.search(cr, uid, [('name', '=', name), ('tesoreria_id', '=', teso.id), ('type', '=', 'in')])
                if saldo_id:
                    saldo = saldos_obj.browse(cr, uid, saldo_id[0])
                    saldos_obj.write(cr, uid, saldo.id, {'saldo': saldo.saldo + math.fabs(pagoR.importe)})
                else:
                    saldos_obj.create(cr, uid, {'name': name, 'saldo': math.fabs(pagoR.importe), 'tesoreria_id': teso.id, 'type':'in'})
            
            for pagoC in teso.pagos_cash:
                if pagoC.payment_type:
                    name = pagoC.payment_type.name
                else:
                    name = 'Undefined'
                saldo_id = saldos_obj.search(cr, uid, [('name', '=', name), ('tesoreria_id', '=', teso.id), ('type', '=', pagoC.type)])
                if saldo_id:
                    saldo = saldos_obj.browse(cr, uid, saldo_id[0])
                    saldos_obj.write(cr, uid, saldo.id, {'saldo': saldo.saldo + math.fabs(pagoC.importe)})
                else:
                    saldos_obj.create(cr, uid, {'name': name, 'saldo': math.fabs(pagoC.importe), 'tesoreria_id': teso.id, 'type':pagoC.type})
            
        return 
    

    def button_calculate(self, cr, uid, ids, context=None):
        facturas_emit = []
        facturas_rec = []
        estado = []
        pagoP_obj = self.pool.get('l10n.es.tesoreria.pagos.period')
        pagoV_obj = self.pool.get('l10n.es.tesoreria.pagos.var')
        pagoR_obj = self.pool.get('l10n.es.tesoreria.pagos.rece')
        pagoC_obj = self.pool.get('l10n.es.tesoreria.pagos.cash')
        t_factura_obj = self.pool.get('l10n.es.tesoreria.facturas')
        invoice_obj = self.pool.get('account.invoice')
        
        self.restart(cr, uid, ids)
        for teso in self.browse(cr, uid, ids):
            if teso.check_draft:
                estado.append("draft")
            if teso.check_proforma:
                estado.append("proforma")
            if teso.check_open:
                estado.append("open")
            invoices = invoice_obj.search(cr, uid, [('date_due', '>=', teso.inicio_validez), ('date_due', '<=', teso.fin_validez), ('state', 'in', tuple(estado))])
            for invoice in invoice_obj.browse(cr, uid, invoices):
                values = {}
                if invoice.type in ('in_invoice', 'out_invoice'):
                    values = {
                        'factura_id': invoice.id,
                        'fecha_vencimiento': invoice.date_due,
                        'partner_id': invoice.partner_id.id,
                        'diario': invoice.journal_id.id,
                        'tipo_pago': invoice.payment_type.id,
                        'payment_term':invoice.payment_term.id,
                        'estado': invoice.state,
                        'base': invoice.amount_untaxed,
                        'impuesto': invoice.amount_tax,
                        'total': invoice.amount_total,
                        'pendiente': invoice.residual,
                    }
                elif invoice.type in ('in_refund', 'out_refund'):
                    values = {
                        'factura_id': invoice.id,
                        'fecha_vencimiento': invoice.date_due,
                        'partner_id': invoice.partner_id.id,
                        'diario': invoice.journal_id.id,
                        'tipo_pago': invoice.payment_type.id,
                        'payment_term':invoice.payment_term.id,
                        'estado': invoice.state,
                        'base': -invoice.amount_untaxed,
                        'impuesto': -invoice.amount_tax,
                        'total': -invoice.amount_total,
                        'pendiente': -invoice.residual,
                    } 
                id = t_factura_obj.create(cr, uid, values)
                if invoice.type == "out_invoice" or invoice.type == "out_refund":
                    facturas_emit.append(id)
                elif invoice.type == "in_invoice" or invoice.type == "in_refund":
                    facturas_rec.append(id)
            self.write(cr, uid, teso.id, {'facturas_emit': [(6, 0, facturas_emit)], 'facturas_rec': [(6, 0, facturas_rec)]})
            for pagoP in teso.plantilla.pagos_period:
                if ((pagoP.fecha >= teso.inicio_validez and pagoP.fecha <= teso.fin_validez) or not pagoP.fecha) and not pagoP.pagado:
                    values = {
                        'name': pagoP.name,
                        'fecha': pagoP.fecha,
                        'partner_id': pagoP.partner_id.id,
                        'payment_type':pagoP.payment_type.id,
                        'importe': pagoP.importe,
                        'tesoreria_id': teso.id,
                    }
                    pagoP_obj.create(cr, uid, values)
            for pagoV in teso.plantilla.pagos_var:
                if ((pagoV.fecha >= teso.inicio_validez and pagoV.fecha <= teso.fin_validez) or not pagoV.fecha) and not pagoV.pagado:
                    values = {
                        'name': pagoV.name,
                        'fecha': pagoV.fecha,
                        'partner_id': pagoV.partner_id.id,
                        'payment_type':pagoV.payment_type.id,
                        'importe': pagoV.importe,
                        'tesoreria_id': teso.id,
                    }
                    pagoV_obj.create(cr, uid, values)
            for pagoR in teso.plantilla.pagos_rece:
                if (pagoR.fecha >= teso.inicio_validez and pagoR.fecha <= teso.fin_validez)or not pagoR.fecha:
                    values = {
                        'name': pagoR.name,
                        'fecha': pagoR.fecha,
                        'diario':pagoR.diario.id,
                        'payment_type':pagoR.payment_type.id,
                        'importe': pagoR.importe,
                        'tesoreria_id': teso.id,
                    }
                    pagoR_obj.create(cr, uid, values)
            for pagoC in teso.plantilla.pagos_cash:
                if (pagoC.fecha >= teso.inicio_validez and pagoC.fecha <= teso.fin_validez)or not pagoC.fecha:
                    values = {
                        'name': pagoC.name,
                        'fecha': pagoC.fecha,
                        'diario':pagoC.diario.id,
                        'payment_type':pagoC.payment_type.id,
                        'importe': pagoC.importe,
                        'type':pagoC.type,
                        'tesoreria_id': teso.id,
                    }
                    pagoC_obj.create(cr, uid, values)
        return True
    def restart(self, cr, uid, ids, context=None):
        
        res = super(l10n_es_tesoreria, self).restart(cr, uid, ids, context)
        
        pagoR_obj = self.pool.get('l10n.es.tesoreria.pagos.rece')
        pagoC_obj = self.pool.get('l10n.es.tesoreria.pagos.cash')
        
        for teso in self.browse(cr, uid, ids):
            for pagoR in teso.pagos_rece:
                pagoR_obj.unlink(cr, uid, pagoR.id)
            for pagoC in teso.pagos_cash:
                pagoC_obj.unlink(cr, uid, pagoC.id)
        return res
l10n_es_tesoreria()

class l10n_es_tesoreria_saldos(osv.osv):
    _name = 'l10n.es.tesoreria.saldos'
    _inherit = 'l10n.es.tesoreria.saldos'
    
    _columns = {
                'type':fields.selection([('in', 'Entrada'), ('out', 'Salida')], 'Tipo', required=True),
                }
l10n_es_tesoreria_saldos()

class l10n_es_tesoreria_pagos_period(osv.osv):
    _name = 'l10n.es.tesoreria.pagos.period'
    _inherit = 'l10n.es.tesoreria.pagos.period'
    _columns = {
                'payment_type': fields.many2one('payment.type', 'Tipo de Pago'),
                }
l10n_es_tesoreria_pagos_period()

class l10n_es_tesoreria_pagos_var(osv.osv):
    _name = 'l10n.es.tesoreria.pagos.var'
    _inherit = 'l10n.es.tesoreria.pagos.var'
    _columns = {
                'payment_type': fields.many2one('payment.type', 'Tipo de Pago'),
                }
l10n_es_tesoreria_pagos_var()

class l10n_es_tesoreria_pagos_cash(osv.osv):
    _name = 'l10n.es.tesoreria.pagos.cash'
    
    def _get_entrada(self, cr, uid, ids, name, args, context=None):
        res = {}
        for cash in self.browse(cr, uid, ids):
            amount = 0.0
            if cash.importe >= 0:
                amount = cash.importe
            res[cash.id] = amount
        return res
    def _get_salida(self, cr, uid, ids, name, args, context=None):
        res = {}
        for cash in self.browse(cr, uid, ids):
            amount = 0.0
            if cash.importe <= 0:
                amount = cash.importe
            res[cash.id] = amount
        return res
            
    _columns = {
                'name': fields.char('Descripción', size=64),
                'fecha': fields.date('Fecha'),
                'diario': fields.many2one('account.journal', 'Diario', domain=[('type', '=', 'purchase')]),
                'importe': fields.float('Importe', digits_compute=dp.get_precision('Account')),
                'payment_type':fields.many2one('payment.type', 'Tipo de Pago'),
                'type':fields.selection([('in', 'Entrada'), ('out', 'Salida')], 'Tipo', required=True),
                'tesoreria_id': fields.many2one('l10n.es.tesoreria', 'Plantilla Tesorería'),
                'entrada': fields.function(_get_entrada, method=True, type='float', string='Entrada', invisible=True),
                'salida': fields.function(_get_salida, method=True, type='float', string='Salida', invisible=True),  
    }
    def _check_importe(self, cr, uid, ids, context=None):
        all_prod = []
        cash = self.browse(cr, uid, ids, context=context)
        res = True
        for flow in cash:
            if flow.type == 'in' and flow.importe <= 0.0:
                res = False
            if flow.type == 'out' and flow.importe >= 0.0:
                res = False
        return res
    
    _constraints = [
        (_check_importe, '\n\nCuidado con las líneas de Cash-Flow!\n Si es de tipo entrada, el importe debe ser positivo.\n Si es de tipo salida, el importe debe ser negativo. ', ['type','importe']),
    ]
l10n_es_tesoreria_pagos_cash()

class l10n_es_tesoreria_pagos_rece(osv.osv):
    _name = 'l10n.es.tesoreria.pagos.rece'
    _columns = {
                'name': fields.char('Descripción', size=64),
                'fecha': fields.date('Fecha'),
                'diario': fields.many2one('account.journal', 'Diario', domain=[('type', '=', 'purchase')]),
                'importe': fields.float('Importe', digits_compute=dp.get_precision('Account')),
                'payment_type':fields.many2one('payment.type', 'Tipo de Pago'),
                'tesoreria_id': fields.many2one('l10n.es.tesoreria', 'Tesorería'),
                } 
l10n_es_tesoreria_pagos_rece()
