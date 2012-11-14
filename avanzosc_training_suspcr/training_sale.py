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

from osv import osv
from osv import fields
from datetime import datetime, timedelta  
from tools.translate import _
import decimal_precision as dp


class training_discount_line(osv.osv):
    _name='training.discount.line'
    _description='Discount Lines'
    _columns = {
            'order_id': fields.many2one('sale.order','Sale Order'),
            'discount_type':fields.many2one('product.product','Discount Type'),
            'discount':fields.float('Discount %'),
            'seance':fields.many2one('training.seance','Seance'),
            'call':fields.integer('Call'),
            'quantity':fields.float('Quantity'),
            'udm':fields.many2one('product.uom','Udm'),
            'price_unit':fields.float('Unit Price'),
            'discount_qty':fields.float('Discount Quantity'),   
    }
training_discount_line()

class sale_order(osv.osv):
    _inherit = "sale.order"
    
    #TRIGGER. 
    def _check_doble_offer(self, cr, uid, ids, context=None):
        #iker
        for sale in self.browse(cr,uid,ids):
            action = True
            if sale.act_par and not sale.offer_id.super_title:
                action=False
            return action      
    
    def _insu_type(self, cr, uid, ids, name, args, context=None):
        res = {}
        for sale in self.browse(cr, uid, ids, context=context):
            age_int=int(sale.contact_age)
            if age_int > 28:
                type="over 28"
            else:
                type="school"
            res[sale.id]=type
        return res
    
    def _recog(self, cr, uid, ids, name, args, context=None):
        res = {}
        recog=False
        for sale in self.browse(cr, uid, ids, context=context):
            for line in sale.order_line:
                if line.product_id.training_charges == 'recog':
                    recog=True
            res[sale.id]=recog
        return res
    
    def _debt(self, cr, uid, ids, name, args, context=None):
        res = {}
        for sale in self.browse(cr, uid, ids, context=context):
            res[sale.id]=sale.amount_total-sale.initial_payment
        return res
    
    
    _columns = {
        'contact_id': fields.many2one('res.partner.contact', 'Student', required=True),
        'session_id':fields.many2one('training.session', 'Session', required = True),
        'session_id2':fields.many2one('training.session', 'Op.Session'),
        'offer_id': fields.many2one('training.offer','Offer', required = True),
        'super_title': fields.related('offer_id','super_title', type='boolean', relation='training.offer', string='Super Title'),
        'act_par': fields.boolean('Acción Pareamiento'),
        'second_cycle': fields.boolean ('Second Cycle'),
        'student_insurance':fields.boolean('Student Insurance'),
        'contact_age': fields.related('contact_id','student_age',type='integer', string='Student age',store=False),        
        'insurance_type':fields.function(_insu_type,type='char',method=True, string='Insurance Type',readonly=True),
        'recog':fields.function(_recog,type='boolean',method=True,string='Recog',readonly=True),
        'discount_line_ids':fields.one2many('training.discount.line','order_id','Discounts',readonly=True),
        'initial_payment':fields.float('Initial Payment'),
        'debt':fields.function(_debt,type='float',method=True,string='Debt',readonly=True),
        }
    _constraints = [
                 (_check_doble_offer,'Error: The Offer is not Double title',['offer_id']),
                 ]
    
    def delete_recog(self, cr, uid, ids,context=None):
        #######################################################################
        #OBJETOS#
        #######################################################################
        sale_order_obj=self.pool.get('sale.order')
        sale_order_line_obj = self.pool.get('sale.order.line')
        training_discount_line_obj=self.pool.get('training.discount.line')
        #######################################################################
        for sale in sale_order_obj.browse(cr, uid,ids):
            found=False
            for line in sale.order_line:
                if line.check:
                    found=True
                    if(line.product_id.training_charges == "recog"):
                        for discount_line in sale.discount_line_ids:
                            discount_type=discount_line.discount_type
                            if line.product_id==discount_type:
                                training_discount_line_obj.unlink(cr, uid,discount_line.id )
                        sale_order_line_obj.unlink(cr, uid,[line.id])
                    else:
                        raise osv.except_osv(_('Error!'),_('Check only recog lines!!'))  
            if not found:
                raise osv.except_osv(_('Error!'),_('Not selected any recog!!'))
        return True
    
    def onchange_partner_id(self, cr, uid, ids, part):
        #iker
        #########################
        ###OBJETOS###
        #####################################################
        partner_obj = self.pool.get('res.partner')
        #####################################################
        val = super(sale_order, self).onchange_partner_id(cr, uid, ids, part)['value']
        if part:
            partner = partner_obj.browse(cr, uid, part)
            if partner.address[0].job_ids[0].contact_id:
                val.update({'contact_id': partner.address[0].job_ids[0].contact_id.id})
        return {'value': val}
    
    def _insert_data_on_record(self, cr, uid, ids, linea, record_id):
        #iker
        ###########################################################
        #orderline = linea
        #existe_expediente[0]  o new_training_record_obj = record_id
        ##################################################################
        training_record_obj = self.pool.get('training.record')
        training_record_line_obj = self.pool.get('training.record.line')
        training_record_credits_line_obj=self.pool.get('training.record.credits.line')
        ###################################################################
        
        line_obj_list =  training_record_line_obj.search(cr, uid, [('record_id', '=' ,record_id)])
        #############
        # Xabi 13/09/2012
         
        ObjSeances=[]
        for lineas in line_obj_list:
            lineas_rec = training_record_line_obj.browse(cr, uid, lineas)
            ObjSeances.append(lineas_rec.seance_id.id)
        #############
        # Xabi 21/08/2012 Creamos estadisticas de creditos en el record
        a=linea.seance_id.name
        a=a.split('(')
        a=a[1]
        a=a.split(')')
        a=a[0]
        session=a[2]+a[3]+'-'+a[7]+a[8]
        valRecCred={
            'record_id':record_id,
            'session':session    
            }
        exists_training_record_credits_line_obj = training_record_credits_line_obj.search(cr, uid, [('session', '=' ,session),('record_id','=',record_id)])
        if  not exists_training_record_credits_line_obj:
            expediente_actual = training_record_obj.browse(cr,uid,record_id)
            objcredit_lines = []
            credit_line_list = expediente_actual.record_credits_line_ids
            for credit_line in credit_line_list:
                objcredit_lines.append(credit_line.id)
            new_training_record_credits_line_obj = training_record_credits_line_obj.create(cr,uid,valRecCred)
            objcredit_lines.append(new_training_record_credits_line_obj)
            training_record_obj.write(cr,uid,record_id,{'record_credits_line_ids': [(6,0,objcredit_lines)]})
        #
        ############
        res=[]
        valRecLine={
            'call':linea.call,
            'state':'not_sub',
            'coursenum_id':linea.coursenum_id.id,
            'mark': 0,
            'date':datetime.now(),
            'year':int(datetime.now().year),
            'name':linea.product_id.name,
            'seance_id': linea.seance_id.id,
            'record_id':record_id,
            'tipology': linea.tipology,
            'type':"ordinary",
            'credits': linea.product_uom_qty,
            'checkrec':False,
            'university':1,
            'course_code':linea.seance_id.course_id.course_code,
            'session':session,
            'cycle': linea.seance_id.course_id.cycle
            }
        #----------------------------------
        # CONVOCATORIA 1
        #----------------------------------
        if linea.call == 1:
            #---------------------------
            # Pareamiento
            #---------------------------
            if linea.matching:
                #print "matching"
                line_id = training_record_line_obj.search(cr, uid, [('seance_id','=',linea.seance_id.id)])
                valRecLine.update({'checkrec':True})
                new_training_record_line_obj = training_record_line_obj.write(cr, uid, line_id, valRecLine )
            #---------------------------
            # Convalidaciónes
            #---------------------------
#            elif linea.convalidate:
#                valRecLine.update({
#                    'state':'recognized',
#                    'mark': 6,
#                    'type':"ordinary",
#                    'checkrec':True,
#                    })
#                
#                if linea.seance_id.id not in ObjSeances:
#                    new_training_record_line_obj = training_record_line_obj.create(cr,uid,valRecLine)
#                    res.append(new_training_record_line_obj) 
            #---------------------------
            # Normal
            #---------------------------
            else:
                valRecLine.update({
                    'state':'not_sub',
                    'mark': 0,
                    'type':"ordinary",
                    })
                new_training_record_line_obj = training_record_line_obj.create(cr,uid,valRecLine)
                res.append(new_training_record_line_obj)
                
                valRecLine.update({
                    'call':linea.call+1,              
                    'state':'not_sub',
                    'mark': 0,
                    'type':"extraordinary",
                    })
                if linea.seance_id.id not in ObjSeances:
                    new_training_record_line_obj = training_record_line_obj.create(cr,uid,valRecLine)
                    res.append(new_training_record_line_obj)
        #----------------------------------
        # CONVOCATORIA 2 y en adelante.
        #---------------------------------- 
        if linea.call > 1:
            #------------------------------
            # Pareamiento
            #------------------------------
            if linea.matching:
                #print "matching"
                line_id = training_record_line_obj.search(cr, uid, [('seance_id','=',linea.seance_id.id)])
                valRecLine.update({'checkrec':True})
                new_training_record_line_obj = training_record_line_obj.write(cr, uid, line_id, valRecLine )
            #---------------------------
            # Convalidaciones
            #---------------------------
#            elif linea.convalidate and linea.price_unit > 0:
#               valRecLine.update({
#                    'state':'recognized',
#                    'mark': 6,
#                    'type':"extraordinary",
#                    'checkrec':True,
#                    })
#               if linea.seance_id.id not in ObjSeances:
#                   new_training_record_line_obj = training_record_line_obj.create(cr,uid,valRecLine)
#                   res.append(new_training_record_line_obj) 
            #---------------------------
            # Teaching (2 insert)
            #---------------------------
            elif linea.teaching:
                valRecLine.update({
                    'state':'not_sub',
                    'mark': 0,
                    'type':"extraordinary",
                    })
                if linea.seance_id.id not in ObjSeances:
                    new_training_record_line_obj = training_record_line_obj.create(cr,uid,valRecLine)
                    res.append(new_training_record_line_obj)
                    
                valRecLine.update({
                    'call':linea.call+1, 
                    'state':'not_sub',
                    'mark': 0,
                    'type':"extraordinary",
                    })
                if linea.seance_id.id not in ObjSeances:
                    new_training_record_line_obj = training_record_line_obj.create(cr,uid,valRecLine)
                    res.append(new_training_record_line_obj)
            #---------------------------
            # Normal (1 insert)
            #---------------------------
            else:
                valRecLine.update({
                    'state':'not_sub',
                    'mark': 0,
                    'type':"extraordinary",
                    })
                if linea.seance_id.id not in ObjSeances:
                    new_training_record_line_obj = training_record_line_obj.create(cr,uid,valRecLine)
                    res.append(new_training_record_line_obj)
        return res
                
    def action_wait(self, cr, uid, ids, *args):
        #iker
        #######################################################################
        #OBJETOS#
        #######################################################################
        training_record_obj = self.pool.get('training.record')
        training_session_obj = self.pool.get('training.session')
        training_seance_obj = self.pool.get('training.seance')
        training_record_line_obj = self.pool.get('training.record.line')
        sale_order_line_obj = self.pool.get('sale.order.line')
        #######################################################################
        for saleorder in self.browse(cr,uid,ids,*args):
            #TITULACION1 --Datos--
            client = saleorder.partner_id.id
            contact = saleorder.contact_id.id
            edition = saleorder.session_id.id
            nombre_edicion = saleorder.session_id.name
            super_title = saleorder.offer_id.super_title
            offer = saleorder.offer_id.id
            offer_obj=saleorder.offer_id
            titulo = saleorder.session_id.offer_id.name
               
        #mirar si exite expediente de ese alumno en esa(s) carreras.
        #-----------------------------
        # Mirar si es Super-titulo
        #-----------------------------
        if super_title:
            sub_title1 = saleorder.offer_id.sub_title1.id
            sub_title2 = saleorder.offer_id.sub_title2.id
            edition1 = saleorder.session_id.id
            edition2 = saleorder.session_id2.id
            #--------------------
            #TITULACION 1 
            #--------------------
            #Existe expediente para la titulacion?
            existe_expediente_title1 = training_record_obj.search(cr,uid,[('student_id','=',contact),('offer_id','=',sub_title1)]) 
            if not existe_expediente_title1:
                valExpediente={
                    'offer_id':sub_title1,
                    'student_id':contact,
                    'edition_ids':[(6,0,[edition1])],
                }
                new_training_record_obj = training_record_obj.create(cr,uid,valExpediente)
                for saleorder in self.browse(cr,uid,ids,*args):
                    list_id_orderlines = sale_order_line_obj.search(cr,uid,[('order_id','=', saleorder.id),('offer_id','=',sub_title1)])
                    for orderline in sale_order_line_obj.browse(cr,uid,list_id_orderlines,*args):
                        if orderline.seance_id:
                        #funcion de crear lineas.
                            self._insert_data_on_record(cr, uid, ids, orderline,new_training_record_obj)
            else:
                 expediente_actual = training_record_obj.browse(cr,uid,existe_expediente_title1[0])
                 objEdicion = []
                 edition_list = expediente_actual.edition_ids
                 for exp_edition in edition_list:
                    objEdicion.append(exp_edition.id)
                 if edition1 not in objEdicion:
                     objEdicion.append(edition1)
                     training_record_obj.write(cr,uid,existe_expediente_title1[0],{'edition_ids':[(6,0,objEdicion)]})
    
                 #INSERTAMOS SEANCES
                 for saleorder in self.browse(cr,uid,ids,*args):
                    list_id_orderlines = sale_order_line_obj.search(cr,uid,[('order_id','=', saleorder.id)])
                    for orderline in sale_order_line_obj.browse(cr,uid,list_id_orderlines,*args):
                        if orderline.seance_id:
                            #funcion de crear lineas.
                            self._insert_data_on_record(cr, uid, ids, orderline, existe_expediente_title1[0])  
                     
            #--------------------         
            # TITULACION 2
            #--------------------    
            existe_expediente_title2 = training_record_obj.search(cr,uid,[('student_id','=',contact),('offer_id','=',sub_title2)])
            if not existe_expediente_title2:
                #Crear Expediente y añadir edición.
                valExpediente={
                    'offer_id':sub_title2,
                    'student_id':contact,
                    'edition_ids':[(6,0,[edition2])],
                }
                new_training_record_obj = training_record_obj.create(cr,uid,valExpediente)
                for saleorder in self.browse(cr,uid,ids,*args):
                    list_id_orderlines_offer2 = sale_order_line_obj.search(cr,uid,[('order_id','=', saleorder.id),('offer_id','=',sub_title2)])
                    for orderline in sale_order_line_obj.browse(cr,uid,list_id_orderlines_offer2,*args):
                        if orderline.seance_id:
                        #funcion de crear lineas.
                            self._insert_data_on_record(cr, uid, ids, orderline,new_training_record_obj)
            else:
                 expediente_actual = training_record_obj.browse(cr,uid,existe_expediente_title2[0])
                 objEdicion = []
                 edition_list = expediente_actual.edition_ids
                 for exp_edition in edition_list:
                    objEdicion.append(exp_edition.id)
                 if edition2 not in objEdicion:
                     objEdicion.append(edition2)
                     training_record_obj.write(cr,uid,existe_expediente_title2[0],{'edition_ids':[(6,0,objEdicion)]})
                     
                 #INSERTAMOS SEANCES
                 for saleorder in self.browse(cr,uid,ids,*args):
                    list_id_orderlines = sale_order_line_obj.search(cr,uid,[('order_id','=', saleorder.id)])
                    for orderline in sale_order_line_obj.browse(cr,uid,list_id_orderlines,*args):
                        if orderline.seance_id:
                            #funcion de crear lineas.
                            self._insert_data_on_record(cr, uid, ids, orderline, existe_expediente_title2[0])
                            
        else:
             #------------------------------------
             #TITULACION ÚNICA (NOT SUPERTITLE)
             #------------------------------------
            existe_expediente = training_record_obj.search(cr,uid,[('student_id','=',contact),('offer_id','=',offer)]) 
            if not existe_expediente:
                #Crear Expediente y añadir edición.
                valExpediente={
                    'offer_id':offer,
                    'student_id':contact,
                    'edition_ids':[(6,0,[edition])],
                    'basic_cycle1':offer_obj.basic_cycle1,
                    'mandatory_cycle1':offer_obj.mandatory_cycle1,
                    'optional_cycle1':offer_obj.optional_cycle1,
                    'freechoice_cycle1':offer_obj.freechoice_cycle1,
                    'basic_cycle2':offer_obj.basic_cycle2,
                    'mandatory_cycle2':offer_obj.mandatory_cycle2,
                    'optional_cycle2':offer_obj.optional_cycle2,
                    'freechoice_cycle2':offer_obj.freechoice_cycle2,
                    'degree_cycle':offer_obj.degree_cycle,
                }
                new_training_record_obj = training_record_obj.create(cr,uid,valExpediente)
            #Una vez creada la edicion recorrer las lineas del pedido ya añadirlas
            #a ese expediente.
                for saleorder in self.browse(cr,uid,ids,*args):
                    list_id_orderlines = sale_order_line_obj.search(cr,uid,[('order_id','=', saleorder.id)])
                    for orderline in sale_order_line_obj.browse(cr,uid,list_id_orderlines,*args):
                        if orderline.seance_id:
                        #funcion de crear lineas.
                            self._insert_data_on_record(cr, uid, ids, orderline,new_training_record_obj)
            else:
            #Mirar si exite edicion anterior de ese usuario para esa titulacion.
                expediente_actual = training_record_obj.browse(cr,uid,existe_expediente[0])
                objEdicion = []
                edition_list = expediente_actual.edition_ids
                for exp_edition in edition_list:
                    objEdicion.append(exp_edition.id)
                if edition not in objEdicion:
                     objEdicion.append(edition)
                     training_record_obj.write(cr,uid,existe_expediente[0],{'edition_ids':[(6,0,objEdicion)]})
                #INSERTAMOS SEANCES
                for saleorder in self.browse(cr,uid,ids,*args):
                        list_id_orderlines = sale_order_line_obj.search(cr,uid,[('order_id','=', saleorder.id)])
                        for orderline in sale_order_line_obj.browse(cr,uid,list_id_orderlines,*args):
                            if orderline.seance_id:
                            #funcion de crear lineas.
                                self._insert_data_on_record(cr, uid, ids, orderline, existe_expediente[0])                         
        val = super(sale_order,self).action_wait(cr,uid,ids,*args)
        return val  
sale_order()

class sale_order_line(osv.osv):
    _inherit = 'sale.order.line'
    
    def _amount_line(self, cr, uid, ids, field_name, arg, context=None):
        #iker
        #Función no se puede heredar, con lo cual la copiamos y la modificamos 
        tax_obj = self.pool.get('account.tax')
        cur_obj = self.pool.get('res.currency')
        res = {}
        if context is None:
            context = {}
        for line in self.browse(cr, uid, ids, context=context):
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
#            print price
#            print line.tax_id
#            print line.product_uom_qty
            taxes = tax_obj.compute_all(cr, uid, line.tax_id, price, line.product_uom_qty, line.order_id.partner_invoice_id.id, line.product_id, line.order_id.partner_id)
#            print taxes
            cur = line.order_id.pricelist_id.currency_id
#            print cur
            valorDevolver = cur_obj.round(cr, uid, cur, taxes['total'])
#            print valorDevolver
#            if line.convalidate:
#                if valorDevolver < 39:
#                    valorDevolver = 39
#                elif valorDevolver > 490:
#                    valorDevolver = 490
#            else:
            #aurreko komentayue kendu ezkeo else barruen dijue hurrengo agindue
            valorDevolver = valorDevolver
            res[line.id] = valorDevolver 
        return res
 
    _columns = {
        'seance_id':fields.many2one('training.seance', 'Seance'),
#        'tipology': fields.related('seance_id','tipology',type='selection',selection=[
#            ('basic', 'Basic'),
#            ('mandatory', 'Mandatory'),
#            ('optional', 'optional'),
#            ('trunk', 'trunk'),
#            ('degreework','Degree Work'),   
#            ],string='Tipology',store=False),
        'tipology': fields.selection([
            ('basic', 'Basic'),
            ('mandatory', 'Mandatory'),
            ('optional', 'optional'),
            ('freechoice','Free Choice'),
            ('trunk', 'trunk'),
            ('complement','Training Complement'),
            ('replacement','Replacement'),
            ('degreework','Degree Work'),   
            ], 'Tipology'),
        'call': fields.integer('Call'),
        'teaching': fields.boolean('Teaching'),
        'convalidate': fields.boolean('Convalidate'),
        'matching': fields.boolean('Matching'),
        'coursenum_id' : fields.many2one('training.coursenum','Number Course'),
        'price_subtotal': fields.function(_amount_line, method=True, string='Subtotal', digits_compute= dp.get_precision('Sale Price')),
        'offer_id': fields.many2one('training.offer','Offer'),
        'session_id':fields.related('order_id','session_id',type='many2one',relation='training.session',string='Session',store=True),
        'contact_id':fields.related('order_id','contact_id',type='many2one',relation='res.partner.contact',string='Contact',store=True),
        'check':fields.boolean('Check'),
    }
    
    def onchange_seance_id(self, cr, uid, ids, seance_id, session_id, contact, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False):
        res = {}
        #OBJETOS
        #-------------------------------------------------------
        seance_obj = self.pool.get('training.seance')
        session_obj = self.pool.get('training.session')
        wizard_obj = self.pool.get('wiz.add.optional.fee')
        record_obj = self.pool.get('training.record')
        #-------------------------------------------------------
        if seance_id:
            seance = seance_obj.browse(cr, uid, seance_id)
            session = session_obj.browse(cr, uid, session_id)
           
            record_id = record_obj.search(cr, uid, [('student_id', '=', contact), ('offer_id', '=', session.offer_id.id)])
            res = self.product_id_change(cr, uid, ids, pricelist, seance.course_id.product_id.id, qty, uom, qty_uos, uos, name, partner_id, lang, update_tax, date_order, packaging, fiscal_position, flag)
            call = wizard_obj._find_call(cr, uid, seance, record_id[0])
            if not call:
                raise osv.except_osv(_('Error!'),_('This subject was passed!'))
            price = wizard_obj._get_subject_price(cr, uid, seance, session, call, teaching=False)
            res['value'].update({
                'tipology': seance.tipology,
                'product_uom_qty': seance.credits,
                'price_unit': price,
                'product_id': seance.course_id.product_id.id,
            })
        return res
    
sale_order_line()