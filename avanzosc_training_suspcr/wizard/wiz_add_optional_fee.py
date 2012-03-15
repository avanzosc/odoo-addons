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
    
    #Como se si es para comvalidar, me falta un parametro.¿?
    def _get_subject_convaldate_price(self, cr, uid, session):
        for price_line in session.price_list:
            if price_line.num_comb == 1:
                return (price_line.price_credit * 5)/100
                
        raise osv.except_osv(_('Error!'),_('There is not a price for call %s in the title: %s') %(str(call),seance.title_id.name))
        return False
                
    
    def _get_subject_price(self, cr, uid, seance, session, call, teaching):
        if call == 0:
            raise osv.except_osv(_('Error!'),_('Call pricelist not found!'))
        
        #TODO: cambioa a lista de precios de la edicion (session)
        for price_line in session.price_list:
            if price_line.num_comb == call:
                if teaching:
                    return price_line.price_credit_teaching
                else:
                    return price_line.price_credit
            
        raise osv.except_osv(_('Error!'),_('There is not a price for call %s in the title: %s') %(str(call),seance.title_id.name))
        return False
    
    def _find_call(self, cr, uid, seance, record_id=False):
         call = 1
         if record_id:
             record = self.pool.get('training.record').browse(cr, uid, record_id)
             for line in record.record_line_ids:
                 if line.session_id.course_id.id == seance.course_id.id:
                     if line.state in ('passed', 'recognized'):
                         return False
                     elif call == line.call and line.state == 'failed':
                         call += 1
                     else:
                         call = line.call
             if call == 7:
                 return False
         return call

 
    _columns = {
        'subject_list': fields.one2many('wiz.training.subject.master', 'wiz_id', 'List of Subjects'),
        'record_id': fields.many2one('training.record', 'Record', readonly=True),
        'session_id': fields.many2one('training.session', 'Session'),
        'fee_list': fields.one2many('wiz.training.fee.master', 'wiz_id', 'List of Fee'),
        'recog_list': fields.one2many('wiz.training.recog.master', 'wiz_id', 'List of Recognition'),
    }
    
    def default_get(self, cr, uid, fields_list, context=None):
        values = {}
        ###########################
        # ARRAYS #
        ###########################
        fee_items = []
        recog_items = []
        seance_items = []
        ###########################
        # OBJETOS #
        ############################
        product_obj = self.pool.get('product.product')
        sale_obj = self.pool.get('sale.order')
        job_obj = self.pool.get('res.partner.job')
        suscr_obj = self.pool.get('training.subscription.line')
        record_obj = self.pool.get('training.record')
        ###########################
        # FEE y RECOG #
        ###########################
        fee_ids = product_obj.search(cr, uid, [('training_charges', '=', 'fee')])
        recog_ids = product_obj.search(cr, uid, [('training_charges', '=', 'recog')])
        sale = sale_obj.browse(cr, uid, context['active_id'])
        seance_ids = []
        if sale.state != 'draft':
            raise osv.except_osv(_('Error!'),_('Sale order not in Draft state!!'))
#        job_id = job_obj.search(cr, uid, [('contact_id', '=', sale.contact_id.id)])
#        suscription_id = suscr_obj.search(cr, uid, [('job_id', '=', job_id)])[0]
#        suscription = suscr_obj.browse(cr, uid, suscription_id)

        record_ids = record_obj.search(cr, uid, [('student_id', '=', sale.contact_id.id), ('offer_id', '=', sale.session_id.offer_id.id)])
        values = {
            'record_id': False,
            'session_id': sale.session_id.id,
        }
        for record in record_obj.browse(cr, uid, record_ids):
            values.update({
                'record_id': record.id,
            })
                                   
        for sale_line in sale.order_line:
            if not sale_line.seance_id.id in seance_ids:
                seance_ids.append(sale_line.seance_id.id)
        for seance in sale.session_id.seance_ids:
            if not seance.id in seance_ids:
                call = self._find_call(cr, uid, seance, values['record_id'])
                if not call:
                    continue
                seance_items.append({
                    'name': seance.name,
                    'product_id': seance.course_id.product_id.id,
                    'seance_id': seance.id,
                    'tipology': seance.tipology,
                    'credits': seance.credits,
#                    'date': seance.date,
                    'call': call,
                    'duration': seance.duration,
                    'state': seance.state,
                    'wiz_id': 1,
                })
                
#        if not 'record_id' in values:
#            raise osv.except_osv(_('Error!'),_('Record not found for this student!'))
            
        for fee in product_obj.browse(cr, uid, fee_ids):
            fee_items.append({
                'name': fee.name,
                'product_id': fee.id,
                'wiz_id': 1,
            })
            
        for recog in product_obj.browse(cr, uid, recog_ids):
            recog_items.append({
                'name': recog.name,
                'product_id': recog.id,
                'wiz_id': 1,
            })
            
        values.update({
            'fee_list': fee_items,
            'recog_list': recog_items,
            'subject_list': seance_items,
        })
        return values
    
    def insert_charge(self, cr, uid, ids, context=None):
        sale_line_obj = self.pool.get('sale.order.line')
        for wiz in self.browse(cr, uid, ids):
            for fee in wiz.fee_list:
                tax_list = []
                if fee.check:
                    values = {
                        'product_id': fee.product_id.id,
                        'name': fee.product_id.name,
                        'price_unit': fee.product_id.list_price,
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
                    values = {
                        'product_id': recog.product_id.id,
                        'name': recog.product_id.name,
                        'price_unit': recog.product_id.list_price,
                        'product_uom': recog.product_id.uom_id.id,
                        'order_id': context['active_id'],
                    }
                    for tax in recog.product_id.taxes_id:
                        tax_list.append(tax.id)
                    if tax_list:
                        values.update({
                            'tax_id': [(6,0,tax_list)]
                        })
                    sale_line_obj.create(cr, uid, values)
            for subject in wiz.subject_list:
                tax_list = []
                if subject.check:
                    if not subject.product_id:
                        raise osv.except_osv(_('Error!'),_('Subject does not have product assigned'))
                    if subject.convalidate:
                        price_unit = self._get_subject_convaldate_price(cr, uid, wiz.session_id)
                    else:
                        price_unit = self._get_subject_price(cr, uid, subject.seance_id, wiz.session_id, subject.call, subject.teaching)
                    values = {
                        'product_id': subject.product_id.id,
                        'name': subject.product_id.name,
                        'tipology': subject.tipology,
                        'call': subject.call,
                        'teaching': subject.teaching,
                        'convalidate': subject.convalidate,
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
        return {'type': 'ir.actions.act_window_close'}
    
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
                ('trunk', 'Trunk'),
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
        'convalidate': fields.boolean('Convalidate'),
        'wiz_id': fields.many2one('wiz.add.optional.fee', 'Wizard'),
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
                'convalidate': False,
            }
        return {'value': res}
    
    def onchange_convalidate(self, cr, uid, ids, convalidate, call, context=None):
        res = {}
        if call == 1:
            res = {
                'teaching': True,
            }
        if convalidate:
            res.update({
                'check': True,
            })
        return {'value': res}
    
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
