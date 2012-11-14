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
from tools.translate import _

class wiz_add_optional_fee(osv.osv_memory):
    _name = 'wiz.add.optional.fee'
    _description = 'Wizard to add optional fee'
    
    def _get_subject_matching_price(self, cr, uid, session):
        #Iker
        for price_line in session.price_list:
            return (price_line.price_credit * 0)
        
        raise osv.except_osv(_('Error!'),_('There is not a price for call %s in the title: %s') %(str(call),seance.title_id.name))
        return False
    
    def _get_subject_convaldate_price(self, cr, uid, session):
        #Urtzi
        for price_line in session.price_list:
            if price_line.num_comb == 1:
                return (price_line.price_credit * 5)/100
                
        raise osv.except_osv(_('Error!'),_('There is not a price for call %s in the title: %s') %(str(call),seance.title_id.name))
        return False
                
    
    def _get_subject_price(self, cr, uid, seance, session, call, teaching):
        #Urtzi
        if call == 0:
            raise osv.except_osv(_('Error!'),_('Call pricelist not found!'))
        
        #TODO: cambioa a lista de precios de la edicion (session)
            
        for price_line in session.price_list:
            if price_line.num_comb == call:
                if teaching:
                    return price_line.price_credit_teaching
                else:
                    return price_line.price_credit
            
        raise osv.except_osv(_('Error!'),_('There is not a price for call %s in the session: %s') %(str(call),session.name))
        return False
    
    def _es_pareamiento(self, cr, uid, mysubscription_id):
        #Urtzi
        ##########################################################
        # OBJETOS #
        ##########################################################
        training_record = self.pool.get('training.record')
        ##########################################################
        es_pareamiento = False
        record_list = training_record.search(cr, uid, [('subscription_id','=',mysubscription_id)])
        if len(record_list) == 2:    
            es_pareamiento = record_list
        else:
            es_pareamiento = False
        return es_pareamiento
    
#    def recorrer_expedientes(self, cr, uid, context):
#        ###########################################################
#        #OBJETOS
#        ##########################################################
#        training_record_obj = self.pool.get('training.record')
#        sale_obj= self.pool.get('sale.order')
#        ##########################################################
#        obj =[]
#        sale = sale_obj.browse(cr, uid, context['active_id'])
#        record_ids = training_record_obj.search(cr, uid, [('student_id', '=', sale.contact_id.id), ('offer_id', '=', sale.session_id.offer_id.id)])
#        for record in record_ids:
#            pareamiento = self._es_pareamiento(cr, uid, record)
#            for record_o in training_record_obj.browse(cr, uid, pareamiento):
#                for record_line in record_o.record_line_ids:
#                    if record_line.state in ('passed', 'recognized'):
#                        if record_line.session_id.course_id.product_id.id not in obj:
#                            obj.append(record_line.session_id.course_id.id)
                        
    def _find_call(self, cr, uid, seance, record_id=False):
        #Urtzi
         call = 1
         no_ass=False
         not_sub=False
         no_school=False
         if record_id:
             record = self.pool.get('training.record').browse(cr, uid, record_id)
             for line in record.record_line_ids:
                 #if line.session_id.course_id.id == seance.course_id.id:
                 if line.seance_id:
                     if line.seance_id.course_id.id == seance.course_id.id:
                         if line.state == 'passed':
                             return False
                         elif call == line.call and line.state in ('passed','merit','distinction'):
                             call += 1
                         elif line.state == 'noassistance':
                             no_ass = True
                         elif line.state == 'not_sub':
                             not_sub = True
                         elif line.state == 'no_schooling':
                             no_school=True
                         else:
                             call = line.call
             if call == 7:
                 #return False
                 call = line.call
         if no_ass:
             return call + 1
         if not_sub:
             return call
         if no_school:
             return call
         else:
             return call
    _columns = {
        'subject_list': fields.one2many('wiz.training.subject.master', 'wiz_id', 'List of Subjects'),
        'record_id': fields.many2one('training.record', 'Record', readonly=True),
        'offer_id': fields.many2one('training.offer', 'Offer', readonly=True),
        'super_title': fields.boolean('Super Title', readonly=True),
        'allowed_degree_anyway': fields.boolean('Allowed degree anyway'),
        'session_id': fields.many2one('training.session', 'Session', readonly=True,),
        'fee_list': fields.one2many('wiz.training.fee.master', 'wiz_id', 'List of Fee'),
        'recog_list': fields.one2many('wiz.training.recog.master', 'wiz_id', 'List of Recognition'),
        'state': fields.selection([
            ('simple','Simple Title'),
            ('double_step_1','Double Title (Step 1)'),
            ('double_step_2','Double Title (Step 2)'),
        ], 'State', readonly=True),
    }
    
    def default_get(self, cr, uid, fields_list, context=None):
        #Urtzi
        values = {}
        ######################################################
        # ARRAYS #
        ######################################################
        fee_items = []
        recog_items = []
        seance_items = []
        ######################################################
        # OBJETOS #
        ######################################################
        product_obj = self.pool.get('product.product')
        sale_obj = self.pool.get('sale.order')
        job_obj = self.pool.get('res.partner.job')
        suscr_obj = self.pool.get('training.subscription.line')
        record_obj = self.pool.get('training.record')
        record_line_obj = self.pool.get('training.record.line')
        ######################################################
        # FEE y RECOG #
        ######################################################
        fee_ids = product_obj.search(cr, uid, [('training_charges', '=', 'fee')])
        recog_ids = product_obj.search(cr, uid, [('training_charges', '=', 'recog')])
        sale = sale_obj.browse(cr, uid, context['active_id'])
        seance_ids = []
        if sale.state != 'draft':
            raise osv.except_osv(_('Error!'),_('Sale order not in Draft state!!'))

        session = sale.session_id
        values = {
            'offer_id': sale.offer_id.id,
            'state': 'simple',
        }
    
        if sale.offer_id.super_title:
            values.update({
                'super_title': 1,
                'state': 'double_step_1',
            })
        if 'state' in context:
            values.update({
                'state': context.get('state'),
            })
            session = sale.session_id2
              
        record_ids = record_obj.search(cr, uid, [('student_id', '=', sale.contact_id.id), ('offer_id', '=', session.offer_id.id)])
        record_id = False
        if record_ids:
            record_id = record_ids[0]    
        values.update({
            'record_id': record_id,
            'session_id': session.id,
        })
                                   
        for sale_line in sale.order_line:
            if not sale_line.seance_id.id in seance_ids:
                seance_ids.append(sale_line.seance_id.id)
                
        if sale.act_par:
            seance_ids = self.find_matched_subjects(cr, uid, seance_ids, sale)
        
        allowed_call_anyway=True
#        allowed_call_anyway=False        
        for seance in session.seance_ids:
            if not seance.id in seance_ids:
                call = self._find_call(cr, uid, seance, values['record_id'])
                if not call:
                    continue
#                elif call == 7 and allowed_call_anyway:
#                    continue
                elif call == 7  and not(allowed_call_anyway):
                    raise osv.except_osv(_('Error!'),_("Spent all calls "))
                elif call > 7:
                    raise osv.except_osv(_('Error!'),_("Spent all calls "))
                seance_items.append({
                    'name': seance.name,
                    'product_id': seance.course_id.product_id.id,
                    'seance_id': seance.id,
                    'coursenum_id':seance.coursenum_id.id,
                    'tipology': seance.tipology,
                    'credits': seance.credits,
#                    'date': seance.date,
                    'call': call,
                    'duration': seance.duration,
                    'state': seance.state,
                    'wiz_id': 1,
                })
        # -> XABI 08/2012
#        ORDENAR LISTAS:
#            por un campo:
#                newlist = sorted(list_to_be_sorted, key=lambda k: k['name'])
#            por mas de un campo:
#        sortedlist = sorted(list_to_be_sorted, key=lambda elem: "%02d %s" % (elem['age'], elem['name'])) 

#        seance_items_sorted=sorted(seance_items, key=lambda k: k['coursenum_id'])
        seance_items_sorted=sorted(seance_items, key=lambda elem: "%02d %s" % (elem['coursenum_id'], elem['name']))
        # XABI 08/2012 <-
#        if not 'record_id' in values:
#            raise osv.except_osv(_('Error!'),_('Record not found for this student!'))
            
        for fee in product_obj.browse(cr, uid, fee_ids):
            fee_items.append({
                'name': fee.name,
                'product_id': fee.id,
                'wiz_id': 1,
            })
            
        for recog in product_obj.browse(cr, uid, recog_ids):
            found=False
            for sale_line in sale.order_line:
                if sale_line.product_id == recog:
                    found=True
            if not found:
                recog_items.append({
                        'name': recog.name,
                        'product_id': recog.id,
                        'wiz_id': 1,
                    })
        values.update({
            'fee_list': fee_items,
            'recog_list': recog_items,
            'subject_list': seance_items_sorted,
        })
        return values
    
    def find_matched_subjects(self, cr, uid, seance_ids, sale, context=None):
        #Urtzi
        seance_obj = self.pool.get('training.seance')
        super_offer = sale.offer_id
        #print 'Seance IDS: '+ str(seance_ids)
        for seance in seance_obj.browse(cr, uid, seance_ids):
            if seance.tipology not in ('mandatory', 'trunk'):
                continue
            
            if seance.offer_id.id == super_offer.sub_title1.id:
                for match_line in super_offer.matching_list:
                    if match_line.course1_id.tipology in ('mandatory', 'basic'):
                        if seance.course_id.id == match_line.course1_id.course_id.id:
                            for match_seance in sale.session_id2.seance_ids:
                                if match_line.course2_id.course_id.id == match_seance.course_id.id:
                                    seance_ids.append(match_seance.id)
                                    
            elif seance.offer_id.id == super_offer.sub_title2.id:
                for match_line in super_offer.matching_list:
                    if match_line.course2_id.tipology in ('mandatory', 'basic'):
                        if seance.course_id.id == match_line.course2_id.course_id.id:
                            for match_seance in sale.session_id1.seance_ids:
                                if match_line.course1_id.course_id.id == match_seance.course_id.id:
                                    seance_ids.append(match_seance.id)
#        print 'New Seance IDS: '+ str(seance_ids)
        return seance_ids
    
    def next_charge(self, cr, uid, ids, context=None):
        #Urtzi
        self.insert_charge(cr, uid, ids,context)
        context.update({
            'state': 'double_step_2',
        })
        return {
                    'type': 'ir.actions.act_window',
                    'res_model': 'wiz.add.optional.fee',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'target': 'new',
                    'context':context
                }
                
    def insert_charge(self, cr, uid, ids,context=None):
        '''
        Insertamos las lineas en sale_order_line
        '''
        #OBJETOS
        ##############################################################
        sale_line_obj = self.pool.get('sale.order.line')
        sale_obj = self.pool.get('sale.order')
        record_obj = self.pool.get('training.record')
        record_line_obj = self.pool.get('training.record.line')
        ##############################################################
        #Urtzi&Iker

        sale = sale_obj.browse(cr, uid, context['active_id'])
        
        for wiz in self.browse(cr, uid, ids):
            
            if sale.act_par:
                offer1 = sale.offer_id.sub_title1.id
                offer2 = sale.offer_id.sub_title2.id
                
                if wiz.state == 'double_step_1':
                    record_line_ids = record_line_obj.search(cr, uid, [('record_id', '=',wiz.record_id.id ),('state','=','recognized'),('checkrec','=', False)])
                    for record_line in record_line_ids:
                            subject = record_line_obj.browse(cr,uid,record_line)
                            val= {
                                  'product_id': subject.session_id.course_id.product_id.id,
                                  'name': subject.session_id.course_id.product_id.name+ _(' (Matched)'),
                                  'offer_id': subject.record_id.offer_id.id,
                                  'tipology': subject.tipology,
                                  'call': subject.call,
                                  'coursenum_id': subject.session_id.coursenum_id.id,
                                  'teaching': False,
                                  'matching':True,
#                                  'convalidate': False,
                                  'seance_id': subject.session_id.id,
                                  'product_uom_qty': 1,
                                  'price_unit': 0,
                                  'product_uom': subject.session_id.course_id.product_id.uom_id.id,
                                  'order_id': context['active_id'],
                            }
                            sale_line_obj.create(cr, uid, val)
                            
                elif wiz.state == 'double_step_2':
                    record_line_ids = record_line_obj.search(cr, uid, [('record_id', '=',wiz.record_id.id ),('state','=','recognized'),('checkrec','=', False)])
                    for record_line in record_line_ids:
                            subject = record_line_obj.browse(cr,uid,record_line)
                            val= {
                                  'product_id': subject.session_id.course_id.product_id.id,
                                  'name': subject.session_id.course_id.product_id.name+ _(' (Matched)'),
                                  'offer_id': subject.record_id.offer_id.id,
                                  'tipology': subject.tipology,
                                  'call': subject.call,
                                  'coursenum_id': subject.session_id.coursenum_id.id,
                                  'teaching': False,
                                  'matching':True,
#                                  'convalidate': False,
                                  'seance_id': subject.session_id.id,
                                  'product_uom_qty': 1,
                                  'price_unit': 0,
                                  'product_uom': subject.session_id.course_id.product_id.uom_id.id,
                                  'order_id': context['active_id'],
                            }
                            sale_line_obj.create(cr, uid, val)
            
            insert_subject = False
            for subject in wiz.subject_list:
                tax_list = []
                if subject.check:
                    if sale.recog:
                        raise osv.except_osv(_('Error!'),_('There is a recog in order lines, remove it first!'))
                    if subject.tipology == 'degreework' and wiz.record_id.progress_rate < 75:
                        insert_subject = True
                        continue
                    if subject.tipology == 'degreework' and wiz.record_id.progress_rate < 75 and allowed_degree_anyway:
                        insert_subject = False
                        continue
                    if not subject.product_id:
                        raise osv.except_osv(_('Error!'),_('Subject does not have product assigned'))
                    #self._insert_select_line(cr, uid, ids, subject, wiz, context)
#                    if subject.convalidate:
#                        price_unit = self._get_subject_convaldate_price(cr, uid, wiz.session_id)
                    if subject.matching:
                        price_unit = self._get_subject_matching_price(cr, uid, wiz.session_id)
                    else:
                        price_unit = self._get_subject_price(cr, uid, subject.seance_id, wiz.session_id, subject.call, subject.teaching)
                    
                    values = {
                        'product_id': subject.product_id.id,
                        'name': subject.product_id.name,
                        'offer_id': subject.seance_id.offer_id.id,
                        'tipology': subject.tipology,
                        'call': subject.call,
                        'coursenum_id': subject.coursenum_id.id,
                        'teaching': subject.teaching,
#                        'convalidate': subject.convalidate,
                        'seance_id': subject.seance_id.id,
                        'product_uom_qty': subject.seance_id.credits,
                        'price_unit': price_unit,
                        'product_uom': subject.product_id.uom_id.id,
                        'order_id': context['active_id'],
                    }
                    for tax in subject.product_id.taxes_id:
                        tax_list.append(tax.id)
                    if tax_list:
                        values.update({
                            'tax_id': [(6,0,tax_list)]
                        })
                    sale_line_obj.create(cr, uid, values)
            if insert_subject == True:
                raise osv.except_osv(_('Error!'),_("Can't do the Degree Work untill you've %75 passed"))
            
            for fee in wiz.fee_list:
                tax_list = []
                if fee.check:
                    values = {
                        'product_id': fee.product_id.id,
                        'name': fee.product_id.name,
                        'tipology':'basic',
                        'offer_id': sale.offer_id.id,
                        'price_unit': 0,
                        'product_uom': fee.product_id.uom_id.id,
                        'order_id': context['active_id'],
                    }
                    for tax in fee.product_id.taxes_id:
                        tax_list.append(tax.id)
                    if tax_list:
                        values.update({
                            'tax_id': [(6,0,tax_list)]
                        })
                    sale_line_obj.create(cr, uid, values)
            for recog in wiz.recog_list:
                tax_list = []
                if recog.check:
                    found=False
                    for line in sale.order_line:
                        if line.product_id.training_charges not in('fee','recog'):
                            found=True
                    if not found:
                        raise osv.except_osv(_('Error!'),_("There is not subject to apply the recog!"))
                    values = {
                        'product_id': recog.product_id.id,
                        'name': recog.product_id.name,
                        'tipology':'basic',
                        'offer_id': sale.offer_id.id,
                        'price_unit': 0,
                        'product_uom': recog.product_id.uom_id.id,
                        'order_id': context['active_id'],
                    }
                    for tax in recog.product_id.taxes_id:
                        tax_list.append(tax.id)
                    if tax_list:
                        values.update({
                            'tax_id': [(6,0,tax_list)]
                        })
                    
                    # -> XABI 08/2012
                    ######################################################
                    # OBJETOS #
                    ######################################################
                    training_offer_type_line_obj = self.pool.get('training.offer.type.line')
                    training_discount_line_obj=self.pool.get('training.discount.line')
                    discount_price=0
                    for line in sale.order_line:
                        if recog.product_id.price_rates:
                            if line.product_uom == recog.product_id.applying_unit and line.product_id.training_charges not in('fee','recog'):
                                offer_type_line_ids=training_offer_type_line_obj.search(cr, uid, [('call', '=', line.call)])
                                offer_type=line.offer_id.offer_type
                                if not offer_type_line_ids:
                                    offer_type=line.offer_id.offer_type.id
                                    offer_type_line_ids=training_offer_type_line_obj.search(cr, uid, [('offer_type', '=', offer_type)])
                                    if not offer_type_line_ids:
                                        raise osv.except_osv(_('Error!'),_('This offer has not got offer type!'))
                                    for price_line in training_offer_type_line_obj.browse(cr,uid,offer_type_line_ids):
                                        price=price_line.price
                                    discount_price-=price*line.product_uom_qty*recog.product_id.discount/100
                                    discount_qty_line=price*line.product_uom_qty*recog.product_id.discount/100
                                else:
                                    has_offer_type=False
                                    for price_line in training_offer_type_line_obj.browse(cr,uid,offer_type_line_ids):
                                        if price_line.offer_type==offer_type:
                                            has_offer_type=True
                                            price=price_line.price
                                            discount_price-=price_line.price*line.product_uom_qty*recog.product_id.discount/100
                                            discount_qty_line=price_line.price*line.product_uom_qty*recog.product_id.discount/100
                                    if not has_offer_type:
                                        raise osv.except_osv(_('Error!'),_('This offer has not got offer type!'))
                                values_discount_line={}
                                values_discount_line.update({'seance':line.seance_id.id,
                                                            'order_id':line.order_id.id,
                                                            'discount_type':recog.product_id.id,
                                                            'discount':recog.product_id.discount,
                                                            'call':line.call,
                                                            'quantity':line.product_uom_qty,
                                                            'udm':line.product_uom.id,
                                                            'price_unit':price,
                                                            'discount_qty':discount_qty_line,
                                                            })                               
                                training_discount_line_obj.create(cr, uid, values_discount_line)
                    values.update({'price_unit': discount_price})
                    sale_line_obj.create(cr, uid, values)
                            
        return {'type': 'ir.actions.act_window_close'}
        # XABI 08/2012 <-
wiz_add_optional_fee()

class wiz_training_subject_master(osv.osv_memory):
    _name = 'wiz.training.subject.master'
    _description = 'Subject Wizard List'
    
    _columns = {
        'name': fields.char('Name', size=64),
        'product_id': fields.many2one('product.product', 'Product', size=64),
        'seance_id': fields.many2one('training.seance', 'Seance'),
        'credits': fields.integer('Credits', required=True, help="Course credits"),
        'tipology': fields.selection([
                ('basic', 'Basic'),
                ('mandatory', 'Mandatory'),
                ('optional', 'Optional'),
                ('freechoice','Free Choice'),
#                ('trunk', 'Trunk'),
                ('degreework','Degree Work'),   
          ], 'Tipology', required=True),
        'call': fields.integer('Call'),
#        'date': fields.datetime('Date'),
        'duration': fields.float('Duration'),
        'state': fields.selection([
            ('opened','Opened'),
            ('confirmed','Confirmed'),
            ('inprogress','In Progress'),
            ('closed','Closed'),
            ('cancelled','Cancelled'),
            ('done','Done'),
        ], 'State'),
        'teaching': fields.boolean('Teaching'),
        'check': fields.boolean('Check'),
#        'convalidate': fields.boolean('Convalidate'),
        'matching': fields.boolean('Matching'),
        'wiz_id': fields.many2one('wiz.add.optional.fee', 'Wizard'),
        'coursenum_id' : fields.many2one('training.coursenum','Number Course'),
        'allowed_call_anyway': fields.boolean('Allowed extra call'),
    }
    
    def onchange_teaching(self, cr, uid, ids, teaching, call, context=None):
        res = {}
        if call == 1:
            res = {
                'teaching': True,
            }
        if teaching:
            res.update({
                'check': True,
            })
        return {'value': res}
    
    def onchange_check(self, cr, uid, ids, check, call, context=None):
        res = {}
        if check and call == 1:
            res = {
                'teaching': True,
            }
        if not check:
            res = {
                'teaching': False,
#                'convalidate': False,
            }
        return {'value': res}
    
#    def onchange_convalidate(self, cr, uid, ids, convalidate, call, context=None):
#        res = {}
#        if call == 1:
#            res = {
#                'teaching': True,
#            }
#        if convalidate:
#            res.update({
#                'check': True,
#            })
#        return {'value': res}
    
wiz_training_subject_master()

class wiz_training_fee_master(osv.osv_memory):
    _name = 'wiz.training.fee.master'
    _description = 'Fee Wizard List'
 
    _columns = {
            'name': fields.char('Description', size=64),
            'product_id': fields.many2one('product.product', 'Product'),
            'check': fields.boolean('Check'),
            'wiz_id': fields.many2one('wiz.add.optional.fee', 'Wizard'),
        }
wiz_training_fee_master()

class wiz_training_recog_master(osv.osv_memory):
    _name = 'wiz.training.recog.master'
    _description = 'Recognition Wizard List'
 
    _columns = {
            'name': fields.char('Description', size=64),
            'product_id': fields.many2one('product.product', 'Product'),
            'check': fields.boolean('Check'),
            'wiz_id': fields.many2one('wiz.add.optional.fee', 'Wizard'),
        }
wiz_training_recog_master()
