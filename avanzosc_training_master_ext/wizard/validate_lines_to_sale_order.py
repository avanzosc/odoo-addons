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

class wiz_validate_lines_to_sale_order(osv.osv_memory):
    _name = 'wiz.validate.lines.to.sale.order'
    _description = 'Wizard to create sale order from validate lines'
    
    _columns = {
        'validate_line_list': fields.one2many('wiz.validate.line', 'wiz_id', 'List of Validate Lines'),
        'note':fields.text('Note',readonly=True),
        'state': fields.selection([
            ('first','First'),
            ('second','Second')
        ], 'State', required=True),
    }
    
    def default_get(self, cr, uid, fields_list, context=None):
        values = {}
        ######################################################
        # OBJETOS #
        ######################################################
        training_record_obj = self.pool.get('training.record')
        validate_items = []
        record = training_record_obj.browse(cr, uid, context['active_id'])
        exists_record_line=False
        for validate_line in record.record_validate_line_ids:
            if not validate_line.order_id:
                validate_items.append({
                        'name': validate_line.name,
                        'validation_type':validate_line.validation_type,
                        'internal_course_id':validate_line.internal_course_id.id,
                        'external_course_id':validate_line.external_course_id.id,
                        'discount_type':validate_line.discount_type,
                        'call':validate_line.call,
                        'check': True,
                        'wiz_id': 1,
                        })
        values.update({
            'state': 'first',
            'validate_line_list': validate_items,
        })
        return values
    
    def next_step(self, cr, uid, ids, context=None):
        values = {}
        ######################################################
        # OBJETOS #
        ######################################################
        training_record_obj = self.pool.get('training.record')
        validate_items = []
        record = training_record_obj.browse(cr, uid, context['active_id'])
        exists_record_line=False
        for wiz in self.browse(cr, uid, ids):
            note=" "
            for validate_line in wiz.validate_line_list:
                for record_line in record.record_line_ids:
                    if validate_line.validation_type=="internal" and record_line.course_code==validate_line.internal_course_id.course_code:
                        if not exists_record_line:
                            exists_record_line=True
                            note='Las siguientes asignaturas que se quieren convalidar ya están en el expediente:' +'\n'+'\n'
                            note=note+'código:'+record_line.course_code+' nombre:'+record_line.name+'\n'
                        else:
                            note=note+'código:'+record_line.course_code+' nombre:'+record_line.name+'\n'
                    elif validate_line.validation_type=="external" and record_line.course_code==validate_line.external_course_id.course_code:
                        if not exists_record_line:
                            exists_record_line=True
                            note='Las siguientes asignaturas que se quieren convalidar ya están en el expediente:' +'\n'+'\n'
                            note=note+'código:'+record_line.course_code+'  nombre:'+record_line.name+'  conv:'+str(record_line.call)+'\n'
                        else:
                            note=note+'código:'+record_line.course_code+' nombre:'+record_line.name+'\n'
        if exists_record_line:
            note=note+'\n'+'Se les va a cambiar el estado a Convalidado. ¿Desea Continuar?'
        else:
            note=note+'Se van a crear las convalidaciones. ¿Desea Continuar?'
        return self.write(cr, uid, ids, {'state': 'second', 'note':note}, context = context)
                
    def create_sale_order(self, cr, uid, ids,context=None):
        #######################################################################
        #OBJETOS#
        #######################################################################
        sale_order_obj=self.pool.get('sale.order')
        sale_order_line_obj = self.pool.get('sale.order.line')
        res_partner_address_obj=self.pool.get('res.partner.address')
        product_pricelist = self.pool.get('product.pricelist')
        training_record_obj=self.pool.get('training.record')
        training_record_line_obj=self.pool.get('training.record.line')
        training_record_validate_line_obj=self.pool.get('training.record.validate.line')
        #######################################################################
        record = training_record_obj.browse(cr, uid, context['active_id'])
        seance=False
        for wiz in self.browse(cr, uid, ids):
            count=0
            for validate_line in wiz.validate_line_list:
                if validate_line.check:
                    count=count+1 
                if validate_line.internal_course_id and not seance:
                    seance=True
                    session=validate_line.internal_course_id.session_ids[0].id
        if not seance:
            session=record.edition_ids[0].id
        if not record.student_id.partner_id.address:
            address=res_partner_address_obj.create(cr,uid,{'partner_id':record.student_id.partner_id.id})
        else:
            address=record.student_id.partner_id.address[0].id
        if not record.student_id.partner_id.property_product_pricelist:
            pricelist=product_pricelist.browse(cr,uid,ids)[0].id
        else:
            pricelist=record.student_id.partner_id.property_product_pricelist.id
        if count > 0:
            val={    
                  'offer_id': record.offer_id.id,
                  'partner_id': record.student_id.partner_id.id,
                  'contact_id': record.student_id.id,
                  'partner_order_id':address,
                  'partner_invoice_id':address,
                  'partner_shipping_id':address,
                  'pricelist_id':pricelist,
                  'picking_police':'direct',
                  'order_policy':'manual',
                  'invoice_quantity':'order',
                  'session_id':session,
                    }
            order_id=sale_order_obj.create(cr, uid, val)
        for wiz in self.browse(cr, uid, ids):
            for validate_line in wiz.validate_line_list:
                if validate_line.check:
                    if validate_line.call==0.0:
                        call=1                    
                    else:
                        call=validate_line.call
                    found=False
                    for price_line in record.offer_id.price_list:
                        if price_line.num_comb ==call:
                            found=True
                            if validate_line.discount_type=='5':
                                price_unit=price_line.price_credit * 5/100
                            elif validate_line.discount_type=='50':
                                price_unit=price_line.price_credit * 50/100
                            elif validate_line.discount_type=='100':
                                price_unit=price_line.price_credit
                            elif validate_line.discount_type=='fixed_50':
                                price_unit=50
                            elif validate_line.discount_type=='exempt':
                                price_unit=0
                    if not found:
                        raise osv.except_osv(_('Error!'),_('There is not a price for one validation'))
                    if validate_line.validation_type=='internal':
                        name=self.pool.get('product.product').name_get(cr, uid, [validate_line.internal_course_id.course_id.product_id.id], context=None)[0][1]
                        vals_line={
                               'internal_course_id':validate_line.internal_course_id.id,
                               'order_id':order_id,
                               'tipology': validate_line.internal_course_id.tipology,
                               'product_uom':validate_line.internal_course_id.course_id.product_id.uom_id.id,
                               'product_uom_qty': validate_line.internal_course_id.credits,
                               'price_unit': price_unit,
                               'product_id': validate_line.internal_course_id.course_id.product_id.id,
                               'course_code': validate_line.internal_course_id.course_id.course_code,
                               'offer_id':record.offer_id.id,
                               'call':call,
                               'name':name,
                               'convalidate':True
                               }
                    else:
                        vals_line={
                               'order_id':order_id,
                               'tipology': validate_line.external_course_id.tipology,
                               'product_uom':validate_line.external_course_id.product_uom_id.id,
                               'product_uom_qty': validate_line.external_course_id.credits,
                               'price_unit': price_unit,
                               'course_code': validate_line.external_course_id.course_code,
                               'offer_id':record.offer_id.id,
                               'call':call,
                               'name':'['+validate_line.external_course_id.course_code+']'+' '+validate_line.external_course_id.name,
                               'convalidate':True
                               }
                    order_line_id=sale_order_line_obj.create(cr, uid, vals_line)
                    for record_validate_line in record.record_validate_line_ids:
                        vals_record_line={
                                            'call':record_validate_line.call,
                                            'state':'not_sub',
                                            'coursenum_id':record_validate_line.coursenum_id.id,
                                            'mark': record_validate_line.mark,
                                            'date':record_validate_line.date,
                                            'year':record_validate_line.year,
                                            'name':record_validate_line.name,
                                            'seance_id': record_validate_line.seance_id.id,
                                            'record_id':record_validate_line.record_id.id,
                                            'tipology': record_validate_line.tipology,
                                            'type':record_validate_line.type,
                                            'credits': record_validate_line.credits,
                                            'checkrec':record_validate_line.checkrec,
                                            'university':record_validate_line.university.id,
                                            'course_code':record_validate_line.course_code,
                                            'session':record_validate_line.session,
                                            'cycle': record_validate_line.cycle,
                                            'order_id':order_id
                                              }
                        if validate_line.validation_type=='internal' and record_validate_line.internal_course_id==validate_line.internal_course_id:
                            validate_line_id=training_record_validate_line_obj.write(cr, uid,record_validate_line.id,{'order_id':order_id})
                            exists_line=False
                            for record_line in record.record_line_ids:
                                if record_line.course_code==record_validate_line.course_code:
                                    exists_line=True
                                    record_line_id=training_record_line_obj.write(cr, uid,record_line.id,{'type':'validated'})
                            if not exists_line:
                                record_line_id=training_record_line_obj.create(cr, uid, vals_record_line)
                        elif validate_line.validation_type=='external' and record_validate_line.external_course_id==validate_line.external_course_id:
                            validate_line_id=training_record_validate_line_obj.write(cr, uid,record_validate_line.id,{'order_id':order_id})
                            exists_line=False
                            for record_line in record.record_line_ids:
                                if record_line.course_code==record_validate_line.course_code:
                                    exists_line=True
                                    record_line_id=training_record_line_obj.write(cr, uid,record_line.id,{'type':'validated'})
                            if not exists_line:
                                record_line_id=training_record_line_obj.create(cr, uid, vals_record_line)
        return {'type': 'ir.actions.act_window_close'}
wiz_validate_lines_to_sale_order()

class wiz_validate_line(osv.osv_memory):
    _name = 'wiz.validate.line'
    _description = 'Validate Line'
 
    _columns = {
            'name':fields.char('Name', size=128),
            'validation_type':fields.selection([('internal', 'Internal'), ('external', 'External')], 'Validation Type'),
            'internal_course_id':fields.many2one('training.seance','Seance'),
            'external_course_id':fields.many2one('training.external.course','External Course'),
            'validate_line_id': fields.many2one('training.record.validate.line', 'Validate Line'),    
            'discount_type':fields.selection([
             ('5','5%'),
             ('50','50%'),
             ('100','100%'),
             ('fixed_50','Fixed 50'),
             ('exempt','Exempt'),],'Discount Type', required=True),
            'call': fields.integer('Call'),
            'check': fields.boolean('Check'),
            'wiz_id': fields.many2one('wiz.delete.recog', 'Wizard'),
        }
wiz_validate_line()