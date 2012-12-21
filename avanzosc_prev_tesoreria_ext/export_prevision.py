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
import pyExcelerator as xl
import csv
import StringIO
class l10n_es_tesoreria(osv.osv):
    _name = 'l10n.es.tesoreria'
    _inherit = 'l10n.es.tesoreria'
    
    
    def export_facturas_emitidas(self, cr , uid, ids, sheet2, context=None):
        if context == None:
            context = {}
        boldFont=xl.Font()
        boldFont.bold=True
        boldS = xl.XFStyle()
        boldS.font = boldFont
        boldFont14=xl.Font()
        boldFont14.bold=True
        boldFont14.height=220
        boldS14 = xl.XFStyle()
        boldS14.font = boldFont14
        numS = xl.XFStyle()
        numS.num_format_str = '#,##0.00'
        tesoreria = self.browse(cr, uid, ids[0])
        sheet2.write(0,0,'FACTURAS EMITIDAS',boldS14)
        sheet2.write(3,0,'FECHA VENCIMIENTO',boldS)
        sheet2.write(3,1,'N. FACTURA',boldS)
        sheet2.write(3,2,'CLIENTE',boldS)
        sheet2.write(3,3,'DIARIO',boldS)
        sheet2.write(3,4,'TIPO DE PAGO',boldS)
        sheet2.write(3,5,'PLAZO DE PAGO',boldS)
        sheet2.write(3,6,'BASE',boldS)
        sheet2.write(3,7,'IMPUESTO',boldS)
        sheet2.write(3,8,'TOTAL',boldS)
        sheet2.write(3,9,'PENDIENTE',boldS)
        sheet2.write(3,10,'ESTADO',boldS)
        lineKont = 5
        for line in tesoreria.facturas_emit:
            if line.factura_id:
                sheet2.write(lineKont,0,line.fecha_vencimiento)
            if line.partner_id:
                sheet2.write(lineKont,1,line.factura_id.number)
            if line.partner_id:
                sheet2.write(lineKont,2,line.partner_id.name)
            if line.diario:
                sheet2.write(lineKont,3,line.diario.name)
            if line.tipo_pago:
                sheet2.write(lineKont,4,line.tipo_pago.name)
            if line.payment_term:
                sheet2.write(lineKont,5,line.payment_term.name)
            sheet2.write(lineKont,6,str(line.base), numS)
            sheet2.write(lineKont,7,str(line.impuesto),numS)
            sheet2.write(lineKont,8,str(line.total),numS)
            sheet2.write(lineKont,9,str(line.pendiente),numS)
            sheet2.write(lineKont,10,line.estado)
            lineKont += 1
        return sheet2
        
    def export_facturas_recibidas(self, cr , uid, ids, sheet3, context=None):
        if context == None:
            context = {} 
        boldFont=xl.Font()
        boldFont.bold=True
        boldS = xl.XFStyle()
        boldS.font = boldFont
        boldFont14=xl.Font()
        boldFont14.bold=True
        boldFont14.height=220
        boldS14 = xl.XFStyle()
        boldS14.font = boldFont14
        numS = xl.XFStyle()
        numS.num_format_str = '#,##0.00'
        tesoreria = self.browse(cr, uid, ids[0])
        sheet3.write(0,0,'FACTURAS RECIBIDAS',boldS14)
        sheet3.write(3,0,'FECHA VENCIMIENTO',boldS)
        sheet3.write(3,1,'N. FACTURA',boldS)
        sheet3.write(3,2,'PROVEEDOR',boldS)
        sheet3.write(3,3,'DIARIO',boldS)
        sheet3.write(3,4,'TIPO DE PAGO',boldS)
        sheet3.write(3,5,'PLAZO DE PAGO',boldS)
        sheet3.write(3,6,'BASE',boldS)
        sheet3.write(3,7,'IMPUESTO',boldS)
        sheet3.write(3,8,'TOTAL',boldS)
        sheet3.write(3,9,'PENDIENTE',boldS)
        sheet3.write(3,10,'ESTADO',boldS)
        lineKont = 5
        for line in tesoreria.facturas_rec:
            if line.factura_id:
                sheet3.write(lineKont,0,line.fecha_vencimiento)
            if line.partner_id:
                sheet3.write(lineKont,1,line.factura_id.number)
            if line.partner_id:
                sheet3.write(lineKont,2,line.partner_id.name)
            if line.diario:
                sheet3.write(lineKont,3,line.diario.name)
            if line.tipo_pago:
                sheet3.write(lineKont,4,line.tipo_pago.name)
            if line.payment_term:
                sheet3.write(lineKont,5,line.payment_term.name)
            sheet3.write(lineKont,6,str(line.base),numS)
            sheet3.write(lineKont,7,str(line.impuesto),numS)
            sheet3.write(lineKont,8,str(line.total),numS)
            sheet3.write(lineKont,9,str(line.pendiente),numS)
            sheet3.write(lineKont,10,line.estado)
            lineKont += 1
        return sheet3
    
    def export_pagos_periodicos(self, cr, uid, ids, sheet4, context=None):
        if context == None:
            context = {} 
        boldFont=xl.Font()
        boldFont.bold=True
        boldS = xl.XFStyle()
        boldS.font = boldFont
        boldFont14=xl.Font()
        boldFont14.bold=True
        boldFont14.height=220
        boldS14 = xl.XFStyle()
        boldS14.font = boldFont14
        numS = xl.XFStyle()
        numS.num_format_str = '#,##0.00'
        tesoreria = self.browse(cr, uid, ids[0])
        sheet4.write(0,0,'PAGOS PERIODICOS',boldS14)
        sheet4.write(3,0,'FECHA',boldS)
        sheet4.write(3,1,'DESCRIPCION',boldS)
        sheet4.write(3,2,'PROVEEDOR',boldS)
        sheet4.write(3,3,'TIPO DE PAGO',boldS)
        sheet4.write(3,4,'IMPORTE',boldS)
        lineKont = 5
        for line in tesoreria.pagos_period:
            if line.fecha:
                sheet4.write(lineKont,0,line.fecha)
            if line.name:
                sheet4.write(lineKont,1,line.name)
            if line.partner_id:
                sheet4.write(lineKont,2,line.partner_id.name)
            if line.payment_type:
                sheet4.write(lineKont,3,line.payment_type.name)
            sheet4.write(lineKont,4,str(line.importe), numS)
            lineKont += 1
        return sheet4
    
    def export_pagos_variables(self, cr, uid, ids, sheet5, context=None):
        if context == None:
            context = {} 
        boldFont=xl.Font()
        boldFont.bold=True
        boldS = xl.XFStyle()
        boldS.font = boldFont
        boldFont14=xl.Font()
        boldFont14.bold=True
        boldFont14.height=220
        boldS14 = xl.XFStyle()
        boldS14.font = boldFont14
        numS = xl.XFStyle()
        numS.num_format_str = '#,##0.00'
        tesoreria = self.browse(cr, uid, ids[0])
        sheet5.write(0,0,'PAGOS VARIABLES', boldS14)
        sheet5.write(3,0,'FECHA',boldS)
        sheet5.write(3,1,'DESCRIPCION',boldS)
        sheet5.write(3,2,'PROVEEDOR',boldS)
        sheet5.write(3,3,'TIPO DE PAGO',boldS)
        sheet5.write(3,4,'IMPORTE',boldS)
        lineKont = 5
        for line in tesoreria.pagos_var:
            if line.fecha:
                sheet5.write(lineKont,0,line.fecha)
            if line.name:
                sheet5.write(lineKont,1,line.name)
            if line.partner_id:
                sheet5.write(lineKont,2,line.partner_id.name)
            if line.payment_type:
                sheet5.write(lineKont,3,line.payment_type.name)
            sheet5.write(lineKont,4,str(line.importe),numS)
            lineKont += 1
        return sheet5
      
    
    def export_cobros_clientes(self, cr, uid, ids, sheet6, context=None):
        if context == None:
            context = {} 
        boldFont=xl.Font()
        boldFont.bold=True
        boldS = xl.XFStyle()
        boldS.font = boldFont
        boldFont14=xl.Font()
        boldFont14.bold=True
        boldFont14.height=220
        boldS14 = xl.XFStyle()
        boldS14.font = boldFont14
        numS = xl.XFStyle()
        numS.num_format_str = '#,##0.00'
        tesoreria = self.browse(cr, uid, ids[0])
        sheet6.write(0,0,'COBROS UNICOS',boldS14)
        sheet6.write(3,0,'FECHA',boldS)
        sheet6.write(3,1,'DESCRIPCION',boldS)
        sheet6.write(3,2,'DIARIO',boldS)
        sheet6.write(3,3,'TIPO DE PAGO',boldS)
        sheet6.write(3,4,'IMPORTE',boldS)
        lineKont = 5
        for line in tesoreria.pagos_rece:
            if line.fecha:
                sheet6.write(lineKont,0,line.fecha)
            if line.name:
                sheet6.write(lineKont,1,line.name)
            if line.diario:
                sheet6.write(lineKont,2,line.diario.name)
            if line.payment_type:
                sheet6.write(lineKont,3,line.payment_type.name)
            sheet6.write(lineKont,4,str(line.importe),numS)
            lineKont += 1
        return sheet6


    def export_cash_flow(self, cr, uid, ids, sheet7, context=None):
        if context == None:
            context = {} 
        boldFont=xl.Font()
        boldFont.bold=True
        boldS = xl.XFStyle()
        boldS.font = boldFont
        boldFont14=xl.Font()
        boldFont14.bold=True
        boldFont14.height=220
        boldS14 = xl.XFStyle()
        boldS14.font = boldFont14
        numS = xl.XFStyle()
        numS.num_format_str = '#,##0.00'
        tesoreria = self.browse(cr, uid, ids[0])
        sheet7.write(0,0,'CASH FLOW',boldS14)
        sheet7.write(3,0,'FECHA',boldS)
        sheet7.write(3,1,'DESCRIPCION',boldS)
        sheet7.write(3,2,'DIARIO',boldS)
        sheet7.write(3,3,'TIPO DE PAGO',boldS)
        sheet7.write(3,4,'TIPO',boldS)
        sheet7.write(3,5,'IMPORTE',boldS)
        lineKont = 5
        for line in tesoreria.pagos_cash:
            if line.fecha:
                sheet7.write(lineKont,0,line.fecha)
            if line.name:
                sheet7.write(lineKont,1,line.name)
            if line.diario:
                sheet7.write(lineKont,2,line.diario.name)
            if line.payment_type:
                sheet7.write(lineKont,3,line.payment_type.name)
            type = 'Entrada'
            if line.type == 'out':
                type = 'Salida'
            sheet7.write(lineKont,4,type)
            sheet7.write(lineKont,5,str(line.importe),numS)
            lineKont += 1
        return sheet7
            
 
    def export_desglose_saldo(self, cr, uid, ids, sheet1, context=None):
        if context == None:
            context = {} 
        boldFont=xl.Font()
        boldFont.bold=True
        boldS = xl.XFStyle()
        boldS.font = boldFont
        boldFont14=xl.Font()
        boldFont14.bold=True
        boldFont14.height=220
        boldS14 = xl.XFStyle()
        boldS14.font = boldFont14
        numS = xl.XFStyle()
        numS.num_format_str = '#,##0.00'
        tesoreria = self.browse(cr, uid, ids[0])
        sheet1.write(11,0,'DESGLOSE SALDO',boldS14)
        sheet1.write(14,0,'TIPO DE PAGO',boldS)
        sheet1.write(14,1,'MODO',boldS)
        sheet1.write(14,2,'IMPORTE',boldS)
        lineKont = 16
        for line in tesoreria.desglose_saldo:
            if line.name:
                sheet1.write(lineKont,0,line.name)
            if line.type == 'in':
                sheet1.write(lineKont,1,'Entrada')
            elif line.type == 'out':
                sheet1.write(lineKont,1,'Salida')
            sheet1.write(lineKont,2,str(line.saldo), numS)
            lineKont += 1
        return sheet1
   
    
    def export_csv(self, cr, uid, ids, context=None):
        adj_obj = self.pool.get('ir.attachment')        
        if context == None:
            context = {}
        tesoreria = self.browse(cr, uid, ids[0])
        fileDoc = xl.Workbook()
        boldFont16=xl.Font()
        boldFont16.bold=True
        boldFont16.height=260
        boldS16 = xl.XFStyle()
        boldS16.font = boldFont16
        boldFont14=xl.Font()
        boldFont14.bold=True
        boldFont14.height=220
        boldS14 = xl.XFStyle()
        boldS14.font = boldFont14
        boldFont=xl.Font()
        boldFont.bold=True
        boldS = xl.XFStyle()
        boldS.font = boldFont
        boldNS = xl.XFStyle()
        boldNS.font = boldFont
        boldNS.num_format_str = '#,##0.00'
        numS = xl.XFStyle()
        numS.num_format_str = '#,##0.00'
        sheet1 = fileDoc.add_sheet("Prevision Tesoreria")
        sheet1.write(1, 0, 'PREVISION TESORERIA',boldS16)
        sheet1.write(4, 0, 'Nombre:',boldS14)
        sheet1.write(4, 1, tesoreria.name,boldS14)
        sheet1.write(4, 3, 'SALDOS',boldS14)
        sheet1.write(6, 0, 'Fecha Inicio:',boldS)
        sheet1.write(6, 1, tesoreria.inicio_validez)
        sheet1.write(6, 3, 'Saldo Inicio:',boldS)
        sheet1.write(6, 4, str(tesoreria.saldo_inicial), numS)
        sheet1.write(7, 0, 'Fecha Final:',boldS)
        sheet1.write(7, 1, tesoreria.fin_validez)
        sheet1.write(7, 3, 'Saldo Final:',boldS)
        sheet1.write(7, 4, str(tesoreria.saldo_final),boldNS)
        if tesoreria.desglose_saldo:
            sheet1 = self.export_desglose_saldo(cr, uid, ids, sheet1, context)
        if tesoreria.facturas_emit:
            sheet2 = fileDoc.add_sheet("Facturas Emitidas")
            sheet2 = self.export_facturas_emitidas(cr, uid, ids, sheet2, context)
        if tesoreria.facturas_rec:
            sheet3 = fileDoc.add_sheet("Facturas Recibidas")
            sheet3 = self.export_facturas_recibidas(cr, uid, ids, sheet3, context)
        if tesoreria.pagos_period:
            sheet4 = fileDoc.add_sheet("Pagos Periodicos")
            sheet4 = self.export_pagos_periodicos(cr, uid, ids, sheet4, context)
        if tesoreria.pagos_var:
            sheet5 = fileDoc.add_sheet("Pagos Variables")
            sheet5 = self.export_pagos_variables(cr, uid, ids, sheet5, context)
        if tesoreria.pagos_rece:
            sheet6 = fileDoc.add_sheet("Cobros Unicos")
            sheet6 = self.export_cobros_clientes(cr, uid, ids, sheet6, context)
        if tesoreria.pagos_cash:
            sheet7 = fileDoc.add_sheet("Cash-Flow")
            sheet7 = self.export_cash_flow(cr, uid, ids, sheet7, context)
        fname = 'Tesoreria_' + tesoreria.name + '.xls'
        file = StringIO.StringIO()
        out = fileDoc.save(file)
        fileDocFin = base64.encodestring(file.getvalue())
        res = {
            'csv_file': fileDocFin,
            'csv_fname': fname }
        wiz_id = self.pool.get('export.csv.wiz').create(cr, uid, res)
        adj_list = adj_obj.search(cr, uid, [('res_id', '=', tesoreria.id), ('res_model', '=', 'l10n.es.tesoreria')])
        kont = 1    
        if adj_list:
            kont = len(adj_list) + 1
            adj_obj.create(cr, uid, {
                                     'name': ('Tesoreria ') + tesoreria.name + ' v.' + str(kont),
                                     'datas': fileDocFin,
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
    
l10n_es_tesoreria()