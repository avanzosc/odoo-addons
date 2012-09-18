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
from osv import osv
from osv import fields
import tools



def safe_unicode(obj, *args):
    """ return the unicode representation of obj """
    try:
        return unicode(obj, *args)
    except UnicodeDecodeError:
        # obj is byte string
        ascii_text = str(obj).encode('utf-8')
        return unicode(ascii_text)
class l10n_es_tesoreria_facturas(osv.osv):
    _name = 'l10n.es.tesoreria.facturas'
    _inherit = 'l10n.es.tesoreria.facturas'
    _columns={
              'inv_type':fields.related('factura_id', 'type', type="selection", selection=[('out_invoice','Customer Invoice'),
            ('in_invoice','Supplier Invoice'),
            ('out_refund','Customer Refund'),
            ('in_refund','Supplier Refund'),], string="Tipo"),
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
                if fact_emit.inv_type == "out_invoice":
                    saldo += fact_emit.total
                if fact_emit.inv_type == "out_refund":
                    saldo -= fact_emit.total
            for fact_rec in teso.facturas_rec:
                if fact_rec.inv_type == "in_invoice":
                    saldo -= fact_rec.total
                if fact_rec.inv_type == "in_refund":
                    saldo += fact_rec.total
            for pagoP in teso.pagos_period:
                saldo -= pagoP.importe
            for pagoV in teso.pagos_var:
                saldo -= pagoV.importe
            for pagoR in teso.pagos_rece:
                saldo += pagoR.importe
            for pagoC in teso.pagos_cash:
                if pagoC.type == "in":
                    saldo += pagoC.importe
                if pagoC.type == "out":
                    saldo -= pagoC.importe
            saldo += teso.saldo_inicial
            res[teso.id] = saldo
        return res
    
    _columns = {
                'pagos_rece':fields.one2many('l10n.es.tesoreria.pagos.rece','tesoreria_id', 'Cobros Unicos'),
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
                if fact_emit.inv_type == 'out_invoice':
                    saldo_id = saldos_obj.search(cr, uid, [('name','=',fact_emit.tipo_pago.name), ('tesoreria_id', '=', teso.id), ('type','=', 'in')])
                    if saldo_id:
                        saldo = saldos_obj.browse(cr, uid, saldo_id[0])
                        saldos_obj.write(cr, uid, saldo.id, {'saldo': saldo.saldo + fact_emit.total})
                    else:
                        saldos_obj.create(cr, uid, {'name': fact_emit.tipo_pago.name, 'saldo': fact_emit.total, 'tesoreria_id': teso.id, 'type':'in'})
                    
                if fact_emit.inv_type == 'out_refund':
                    saldo_id = saldos_obj.search(cr, uid, [('name','=',fact_emit.tipo_pago.name), ('tesoreria_id', '=', teso.id), ('type','=', 'out')])
                    if saldo_id:
                        saldo = saldos_obj.browse(cr, uid, saldo_id[0])
                        saldos_obj.write(cr, uid, saldo.id, {'saldo': saldo.saldo + fact_emit.total})
                    else:
                        saldos_obj.create(cr, uid, {'name': fact_emit.tipo_pago.name, 'saldo': fact_emit.total, 'tesoreria_id': teso.id, 'type':'out'})
            for fact_rec in teso.facturas_rec:
                if fact_rec.inv_type == 'in_invoice':
                    saldo_id = saldos_obj.search(cr, uid, [('name','=',fact_rec.tipo_pago.name), ('tesoreria_id', '=', teso.id),('type','=','out')])
                    if saldo_id:
                        saldo = saldos_obj.browse(cr, uid, saldo_id[0])
                        saldos_obj.write(cr, uid, saldo.id, {'saldo': saldo.saldo + fact_rec.total})
                    else:
                        saldos_obj.create(cr, uid, {'name': fact_rec.tipo_pago.name, 'saldo': fact_rec.total, 'tesoreria_id': teso.id, 'type':'out'})
                if fact_rec.inv_type == 'in_refund':
                    saldo_id = saldos_obj.search(cr, uid, [('name','=',fact_rec.tipo_pago.name), ('tesoreria_id', '=', teso.id),('type','=','in')])
                    if saldo_id:
                        saldo = saldos_obj.browse(cr, uid, saldo_id[0])
                        saldos_obj.write(cr, uid, saldo.id, {'saldo': saldo.saldo + fact_rec.total})
                    else:
                        saldos_obj.create(cr, uid, {'name': fact_rec.tipo_pago.name, 'saldo': fact_rec.total, 'tesoreria_id': teso.id, 'type':'in'})
            for pagoV in teso.pagos_var:
                if pagoV.payment_type:
                    name = pagoV.payment_type.name
                else:
                    name='Undefined'
                saldo_id = saldos_obj.search(cr, uid, [('name','=',name), ('tesoreria_id', '=', teso.id),('type','=','out')])
                if saldo_id:
                    saldo = saldos_obj.browse(cr, uid, saldo_id[0])
                    saldos_obj.write(cr, uid, saldo.id, {'saldo': saldo.saldo + pagoV.importe})
                else:
                    saldos_obj.create(cr, uid, {'name': name, 'saldo': pagoV.importe, 'tesoreria_id': teso.id, 'type':'out'})
            for pagoP in teso.pagos_period:
                if pagoP.payment_type:
                    name = pagoP.payment_type.name
                else:
                    name='Undefined'
                saldo_id = saldos_obj.search(cr, uid, [('name','=',name), ('tesoreria_id', '=', teso.id),('type','=','out')])
                if saldo_id:
                    saldo = saldos_obj.browse(cr, uid, saldo_id[0])
                    saldos_obj.write(cr, uid, saldo.id, {'saldo': saldo.saldo + pagoP.importe})
                else:
                    saldos_obj.create(cr, uid, {'name': name, 'saldo': pagoP.importe, 'tesoreria_id': teso.id, 'type':'out'})
            for pagoR in teso.pagos_rece:
                if pagoR.payment_type:
                    name = pagoR.payment_type.name
                else:
                    name='Undefined'
                saldo_id = saldos_obj.search(cr, uid, [('name','=',name), ('tesoreria_id', '=', teso.id),('type','=','in')])
                if saldo_id:
                    saldo = saldos_obj.browse(cr, uid, saldo_id[0])
                    saldos_obj.write(cr, uid, saldo.id, {'saldo': saldo.saldo + pagoR.importe})
                else:
                    saldos_obj.create(cr, uid, {'name': name, 'saldo': pagoR.importe, 'tesoreria_id': teso.id, 'type':'in'})
            
            for pagoC in teso.pagos_cash:
                if pagoC.payment_type:
                    name = pagoC.payment_type.name
                else:
                    name='Undefined'
                saldo_id = saldos_obj.search(cr, uid, [('napagos_cashme','=',name), ('tesoreria_id', '=', teso.id),('type','=',pagoC.type)])
                if saldo_id:
                    saldo = saldos_obj.browse(cr, uid, saldo_id[0])
                    saldos_obj.write(cr, uid, saldo.id, {'saldo': saldo.saldo + pagoC.importe})
                else:
                    saldos_obj.create(cr, uid, {'name': name, 'saldo': pagoC.importe, 'tesoreria_id': teso.id, 'type':pagoC.type})
            
        return 
    
    def export_facturas_emitidas(self, cr ,uid, ids, csv_tesoreria,context=None):
        if context == None:
            context = {}
        tesoreria = self.browse(cr, uid, ids[0])
	pre_text = ''
        pre_text += 'FACTURAS EMITIDAS'
        pre_text += '\r\n'
        pre_text += '\r\n'
        pre_text += 'FECHA VENCIMIENTO,Nº FACTURA,CLIENTE,DIARIO,TIPO DE PAGO,PLAZO DE PAGO,BASE,IMPUESTO,TOTAL,ESTADO'
        pre_text += '\r\n'
	pre_text = tools.ustr(pre_text)
	csv_tesoreria += pre_text
        for line in tesoreria.facturas_emit:
            text = ''
            text += line.fecha_vencimiento + ','
            if line.factura_id:
                text += '\"' + line.factura_id.number + '\"'
            text += ','
            if line.partner_id:
                text += '\"' + line.partner_id.name + '\"'
            text += ','
            if line.diario:
                text += '\"' + line.diario.name + '\"'
            text += ','
            if line.tipo_pago:
                text += '\"' + line.tipo_pago.name + '\"'
            text += ','
            if line.payment_term:
                text += '\"' + line.payment_term.name + '\"'
            text += ','
            text += str(line.base) + ','
            text += str(line.impuesto) + ','
            text += str(line.total) + ','
            text += line.estado + ','
	    text += '\r\n'
	    text = tools.ustr(text)
            csv_tesoreria += text
	post_text = ''        
	post_text += '\r\n'
        post_text += '\r\n'
        post_text += '\r\n'
	post_text = tools.ustr(post_text)
	csv_tesoreria += post_text
        return csv_tesoreria
        
    def export_facturas_recibidas(self, cr ,uid, ids, csv_tesoreria,context=None):
        if context == None:
            context = {} 
        tesoreria = self.browse(cr, uid, ids[0])
	pre_text = ''        
	pre_text += 'FACTURAS RECIBIDAS'
        pre_text += '\r\n'
        pre_text += '\r\n'
        pre_text += 'FECHA VENCIMIENTO,Nº FACTURA,PROVEEDOR,DIARIO,TIPO DE PAGO,PLAZO DE PAGO,BASE,IMPUESTO,TOTAL,ESTADO'
        pre_text += '\r\n'
	pre_text = tools.ustr(pre_text)
	csv_tesoreria += pre_text
        for line in tesoreria.facturas_rec:
            text = ''
            text += line.fecha_vencimiento + ','
            if line.factura_id:
                text += '\"' + line.factura_id.number + '\"'
            text += ','
            if line.partner_id:
                text += '\"' + line.partner_id.name + '\"'
            text += ','
            if line.diario:
                text += '\"' + line.diario.name + '\"'
            text += ','
            if line.tipo_pago:
                text += '\"' + line.tipo_pago.name + '\"'
            text += ','
            if line.payment_term:
                text += '\"' + line.payment_term.name + '\"'
            text += ','
            text += str(line.base) + ','
            text += str(line.impuesto) + ','
            text += str(line.total) + ','
            text += line.estado + ','
	    text += '\r\n'
	    text = tools.ustr(text)
            csv_tesoreria += text
        post_text = ''        
	post_text += '\r\n'
        post_text += '\r\n'
        post_text += '\r\n'
	post_text = tools.ustr(post_text)
	csv_tesoreria += post_text
        return csv_tesoreria
    
    def export_pagos_periodicos(self, cr, uid, ids, csv_tesoreria, context=None):
        if context == None:
            context = {} 
        tesoreria = self.browse(cr, uid, ids[0])
        if tesoreria.pagos_period:
	    pre_text = ''
            pre_text += 'PAGOS PERIODICOS'
            pre_text += '\r\n'
            pre_text += '\r\n'
            pre_text += 'FECHA,DESCRIPCIÓN,PROVEEDOR,TIPO DE PAGO,IMPORTE'
            pre_text += '\r\n'
	    pre_text = tools.ustr(pre_text)
	    csv_tesoreria += pre_text
            for line in tesoreria.pagos_period:
                text = ''
                if line.fecha:
                    text += line.fecha 
                text += ','
                if line.name:
                    text += '\"' + line.name + '\"'
                text += ','
                if line.partner_id:
                    text += '\"' + line.partner_id.name + '\"'
                text += ','
                if line.payment_type:
                    text += '\"' + line.payment_type.name + '\"'
                text += ','
                text += str(line.importe) + ','
                text += '\r\n'
	    	text = tools.ustr(text)
            	csv_tesoreria += text
            post_text = ''        
	    post_text += '\r\n'
            post_text += '\r\n'
            post_text += '\r\n'
	    post_text = tools.ustr(post_text)
	    csv_tesoreria += post_text
        return csv_tesoreria
    
    def export_pagos_variables(self, cr, uid, ids, csv_tesoreria, context=None):
        if context == None:
            context = {} 
        tesoreria = self.browse(cr, uid, ids[0])
        if tesoreria.pagos_var:
	    pre_text = ''
            pre_text += 'PAGOS VARIABLES'
            pre_text += '\r\n'
            pre_text += '\r\n'
            pre_text += 'FECHA,DESCRIPCIÓN,PROVEEDOR,TIPO DE PAGO,IMPORTE'
            pre_text += '\r\n'
	    pre_text = tools.ustr(pre_text)
	    csv_tesoreria += pre_text
            for line in tesoreria.pagos_var:
                text = ''
                if line.fecha:
                    text += line.fecha 
                text += ','
                if line.name:
                    text += '\"' + line.name + '\"'
                text += ','
                if line.partner_id:
                    text += '\"' + line.partner_id.name + '\"'
                text += ','
                if line.payment_type:
                    text += '\"' + line.payment_type.name + '\"'
                text += ','
                text += str(line.importe) + ','
		text += '\r\n'
	    	text = tools.ustr(text)
            	csv_tesoreria += text
            post_text = ''        
	    post_text += '\r\n'
            post_text += '\r\n'
            post_text += '\r\n'
	    post_text = tools.ustr(post_text)
	    csv_tesoreria += post_text
        return csv_tesoreria
      
    
    def export_cobros_clientes(self, cr, uid, ids, csv_tesoreria, context=None):
        if context == None:
            context = {} 
        tesoreria = self.browse(cr, uid, ids[0])
        if tesoreria.pagos_rece:
	    pre_text = ''
            pre_text += 'COBROS CLIENTES'
            pre_text += '\r\n'
            pre_text += '\r\n'
            pre_text += 'FECHA,DESCRIPCIÓN,DIARIO,TIPO DE PAGO,IMPORTE'
            pre_text += '\r\n'
	    pre_text = tools.ustr(pre_text)
	    csv_tesoreria += pre_text
            for line in tesoreria.pagos_rece:
                text = ''
                if line.fecha:
                    text += line.fecha 
                text += ','
                if line.name:
                    text += '\"' + line.name + '\"'
                text += ','
                if line.diario:
                    text += '\"' + line.diario.name + '\"'
                text += ','
                if line.payment_type:
                    text += '\"' + line.payment_type.name + '\"'
                text += ','
                text += str(line.importe) + ','
		text += '\r\n'
	    	text = tools.ustr(text)
            	csv_tesoreria += text
            post_text = ''        
	    post_text += '\r\n'
            post_text += '\r\n'
            post_text += '\r\n'
	    post_text = tools.ustr(post_text)
	    csv_tesoreria += post_text
        return csv_tesoreria


    def export_cash_flow(self, cr, uid, ids, csv_tesoreria, context=None):
        if context == None:
            context = {} 
        tesoreria = self.browse(cr, uid, ids[0])
        if tesoreria.pagos_cash:
	    pre_text = ''
            pre_text += 'CASH FLOW'
            pre_text += '\r\n'
            pre_text += '\r\n'
            pre_text += 'FECHA,DESCRIPCIÓN,DIARIO,TIPO DE PAGO,TIPO,IMPORTE'
            pre_text += '\r\n'
	    pre_text = tools.ustr(pre_text)
	    csv_tesoreria += pre_text
            for line in tesoreria.pagos_cash:
                text = ''
                if line.fecha:
                    text += line.fecha 
                text += ','
                if line.name:
                    text += '\"' + line.name + '\"'
                text += ','
                if line.diario:
                    text += '\"' + line.diario.name + '\"'
                text += ','
                if line.payment_type:
                    text += '\"' + line.payment_type.name + '\"'
                text += ','
                if line.type == 'in':
                    text += '\"' + 'Entrada' + '\"'
                elif line.type == 'out':
                    text += '\"' + 'Salida' + '\"'
                text += ','
                text += str(line.importe) + ','
		text += '\r\n'
	    	text = tools.ustr(text)
            	csv_tesoreria += text
            post_text = ''        
	    post_text += '\r\n'
            post_text += '\r\n'
            post_text += '\r\n'
	    post_text = tools.ustr(post_text)
	    csv_tesoreria += post_text
        return csv_tesoreria
        	
 
    def export_desglose_saldo(self, cr, uid, ids, csv_tesoreria, context=None):
        if context == None:
            context = {} 
        tesoreria = self.browse(cr, uid, ids[0])
        if tesoreria.desglose_saldo:
	    pre_text = ''
            pre_text += 'DESGLOSE SALDO'
            pre_text += '\r\n'
            pre_text += '\r\n'
            pre_text += 'TIPO DE PAGO,MODO,IMPORTE'
            pre_text += '\r\n'
	    pre_text = tools.ustr(pre_text)
	    csv_tesoreria += pre_text
            for line in tesoreria.desglose_saldo:
                text = ''
                if line.name:
                    text += '\"' + line.name + '\"'
                text += ','
                if line.type == 'in':
                    text += '\"' + 'Entrada' + '\"'
                elif line.type == 'out':
                    text += '\"' + 'Salida' + '\"'
                text += ','
                text += str(line.saldo) + ','
		text += '\r\n'
	    	text = tools.ustr(text)
            	csv_tesoreria += text
            post_text = ''        
	    post_text += '\r\n'
            post_text += '\r\n'
            post_text += '\r\n'
	    post_text = tools.ustr(post_text)
	    csv_tesoreria += post_text
        return csv_tesoreria
   
    
    def export_csv(self, cr, uid, ids, context= None):
	adj_obj = self.pool.get('ir.attachment')        

	if context == None:
            context = {}
        tesoreria = self.browse(cr, uid, ids[0])
        
        
        
        csv_tesoreria = 'PREVISION TESORERIA'
        csv_tesoreria += '\r\n'
        csv_tesoreria += '\r\n'
        csv_tesoreria += 'Nombre:,' + tesoreria.name + ',,SALDOS'
        csv_tesoreria += '\r\n'
        csv_tesoreria += 'Fecha Inicio:,' + tesoreria.inicio_validez + ',,Saldo Inicio:,' + str(tesoreria.saldo_inicial)
        csv_tesoreria += '\r\n'
        csv_tesoreria += 'Fecha Final:,' + tesoreria.fin_validez + ',,Saldo Final:,' + str(tesoreria.saldo_final)
        csv_tesoreria += '\r\n'
        csv_tesoreria += '\r\n'
        csv_tesoreria += '\r\n'
        csv_tesoreria = self.export_desglose_saldo(cr,uid,ids,csv_tesoreria,context)
        csv_tesoreria = self.export_facturas_emitidas(cr,uid,ids,csv_tesoreria,context)
        csv_tesoreria = self.export_facturas_recibidas(cr,uid,ids,csv_tesoreria,context)
        csv_tesoreria = self.export_pagos_periodicos(cr,uid,ids,csv_tesoreria,context)
        csv_tesoreria = self.export_pagos_variables(cr,uid,ids,csv_tesoreria,context)
        csv_tesoreria = self.export_cobros_clientes(cr,uid,ids,csv_tesoreria,context)
        csv_tesoreria = self.export_cash_flow(cr,uid,ids,csv_tesoreria,context)
        

        csv_tesoreria = csv_tesoreria.replace('\r\n','\n').replace('\n','\r\n')
        file = base64.encodestring(csv_tesoreria.encode('utf-8'))
        fname = 'Tesoreria_' + tesoreria.name + '.csv'
        res =  {
            'csv_file': file, 
            'csv_fname': fname }
        wiz_id = self.pool.get('export.csv.wiz').create(cr,uid,res)
        adj_list = adj_obj.search(cr,uid,[('res_id', '=', tesoreria.id), ('res_model', '=', 'l10n.es.tesoreria')])
	kont = 1	
	if adj_list:
		kont = len(adj_list) + 1
        adj_obj.create(cr, uid, {
            'name': ('Tesoreria ') + tesoreria.name + ' v.' + str(kont),
            'datas': file,
            'datas_fname': fname,
            'res_model': 'l10n.es.tesoreria',
            'res_id': tesoreria.id,
            }, context=context)
        
        return {
                'type': 'ir.actions.act_window',
                'res_model': 'export.csv.wiz',
                'view_type': 'form',
                'view_mode': 'form',
                'nodestroy': True,
                'res_id': wiz_id,
                'target': 'new',
                }
    
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
            invoices = invoice_obj.search(cr, uid, [('date_due', '>', teso.inicio_validez), ('date_due', '<', teso.fin_validez), ('state', 'in', tuple(estado))])
            for invoice in invoice_obj.browse(cr, uid, invoices):
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
                id = t_factura_obj.create(cr, uid, values)
                if invoice.type == "out_invoice" or invoice.type == "out_refund":
                    facturas_emit.append(id)
                elif invoice.type == "in_invoice" or invoice.type == "in_refund":
                    facturas_rec.append(id)
            self.write(cr, uid, teso.id, {'facturas_emit': [(6,0, facturas_emit)], 'facturas_rec': [(6,0, facturas_rec)]})
            for pagoP in teso.plantilla.pagos_period:
                if ((pagoP.fecha > teso.inicio_validez and pagoP.fecha < teso.fin_validez) or not pagoP.fecha) and not pagoP.pagado:
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
                if ((pagoV.fecha > teso.inicio_validez and pagoV.fecha < teso.fin_validez) or not pagoV.fecha) and not pagoV.pagado:
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
                if (pagoR.fecha > teso.inicio_validez and pagoR.fecha < teso.fin_validez)or not pagoR.fecha:
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
                if (pagoC.fecha > teso.inicio_validez and pagoC.fecha < teso.fin_validez)or not pagoC.fecha:
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
        
        res = super(l10n_es_tesoreria,self).restart(cr,uid,ids,context)
        
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
                'type':fields.selection([('in','Entrada'),('out','Salida')], 'Tipo', required=True),
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
    _columns = {
                'name': fields.char('Descripción', size=64),
                'fecha': fields.date('Fecha'),
                'diario': fields.many2one('account.journal', 'Diario', domain=[('type', '=', 'purchase')]),
                'importe': fields.float('Importe', digits_compute=dp.get_precision('Account')),
                'payment_type':fields.many2one('payment.type', 'Tipo de Pago'),
                'type':fields.selection([('in', 'Entrada'),('out','Salida')],'Tipo', required=True),
                'tesoreria_id': fields.many2one('l10n.es.tesoreria', 'Plantilla Tesorería'),
    }
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
