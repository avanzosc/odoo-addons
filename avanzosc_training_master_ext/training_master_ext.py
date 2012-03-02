
# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2004-2010 Tiny SPRL (http://tiny.be). All Rights Reserved
#    
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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
from osv import osv, fields

class training_credit_prices(osv.osv):
    _name='training.credit.prices'
    _description='credit prices'
    _columns = {
            'num_comb': fields.integer('Num.Combo'),
            'price_credit': fields.float('Price per Credit'),
            
            }
training_credit_prices()

class training_titles(osv.osv):
    _name='training.titles'
    _description='titles'
    _columns = {
            'title_id':fields.char('Code', size=64, required = True),
            'name':fields.char('Name',size=64),
            'price_list':fields.one2many('training.credit.prices','title_id','Prices per Credit')
            }
training_titles()

class training_credit_prices(osv.osv):
    _inherit='training.credit.prices'
    
    _columns = {
            'title_id': fields.many2one('training.titles','Titles'),
            }
training_credit_prices()

class training_source(osv.osv):
    _name='training.source'
    _description='source'
    _columns = {
            'code':fields.char('Reference',size=64),
            'name':fields.char('Name',size=64),
            }
training_source()

class training_coursenum(osv.osv):
    _name='training.coursenum'
    _description='coursenum'
    _columns = {
            'code':fields.integer('Reference',size=64),
            'name':fields.char('name',size=64),
    }
training_coursenum()

class training_universities(osv.osv):
    _name='training.universities'
    _description='universities'
    _columns = {
            'code':fields.char('Reference',size=64),
            'name':fields.char('Name',size=64),
            }
training_universities()

class training_offer(osv.osv):
    _inherit = 'training.offer'
    
    #OnChange
    def onchange_title_id(self, cr, uid, ids, title_id, context=None):
        ##########################################################
        training_title_obj = self.pool.get('training.titles')
        ##########################################################
        res = {}
        if title_id:
           val= training_title_obj.browse(cr,uid,title_id,context=None).name
        res = {'name': val}
        return {'value': res}
       
    _columns = {
            'active': fields.boolean('Activo'),
            'numhours': fields.integer('Num.Horas',size=2),
            'letter': fields.char('Letra', size=64),
            'shortname': fields.char('Nombre corto', size=64),
            'numcursos': fields.integer('Num Cursos'), 
            'impcredito': fields.integer('Imp Credito'),
            'gradoexp': fields.integer('Grado Exp'),
            'title_id': fields.many2one('training.titles','Title'),
			'title_id2': fields.many2one('training.titles','Title Additional'),
            'boe': fields.char('boe',size=64),
            'textoboe': fields.text('TextBOE',size=64),                   
            } 
    _defaults = { 'active': lambda *a : True,}
training_offer() 

class training_course(osv.osv):
    _inherit ='training.course'
   
    _columns= {
        'course_code': fields.char('Course Code', size=32, required=True),
   	    'resolution': fields.char('Resolution', size=64),
        'boedate': fields.datetime('BOE Date', required=True),
        'subjecteng': fields.char('Asignatura Eng', size=64),
        'ects': fields.integer('ECTS'),
        'product_id':fields.many2one('product.product', 'Product'),
        'tipo_docencia':fields.selection([('F', 'F'),('L', 'L'),('N', 'N'),('X', 'X')], 'Type teaching', required=True),
		'credits': fields.integer('Credits', required=True, help="Course credits"),	
		'offer_ids' : fields.one2many('training.course.offer.rel', 'course_id', 'Offers', help='A course could be included on some offers'),
		'seance_ids' : fields.one2many('training.seance', 'course_id', 'Offers', help='A course could generate some seances'),
        'coursenum_id' : fields.many2one('training.coursenum','Number Course'),
        'semester': fields.selection([('first_semester','First Semester'),('second_semester','Second Semester')],'Semester',required=True),
        }    
training_course()

class training_course_offer_rel(osv.osv):
    _inherit = 'training.course.offer.rel'

    _columns = {
        'tipology': fields.selection([('mandatory', 'mandatory'),('trunk', 'trunk'),('optional', 'optional'),('free', 'free'),('complementary', 'complementary'),('replace', 'replace')], 'Tipology', required=True),
        }
training_course_offer_rel()

class training_subscription(osv.osv):
    _inherit = 'training.subscription'
    
    _columns = {
        'universities':fields.many2one('training.universities','Universities'),
        'source':fields.many2one('training.source','Source')
        }
    _defaults = {
        'name': lambda self,cr,uid,context={}: self.pool.get('ir.sequence').get(cr, uid, 'training.suscription'),
            }
training_subscription()

class training_subscription_line(osv.osv):
    _inherit = 'training.subscription.line'
    
    _columns = {
        'code':fields.many2one('training.coursenum','coursenum')
     }
training_subscription_line()

class sale_order(osv.osv):
    _inherit = 'sale.order'
 
    _columns = {
        'session_id': fields.many2one('training.session', 'Session', required=True),
        #'session_id2': fields.many2one('training.session', 'Session', required=False),
    }
sale_order()

class sale_order_line(osv.osv):
    _inherit = 'sale.order.line'
 
    _columns = {
        'seance_id': fields.many2one('training.seance', 'Seance', required=True),
        'call': fields.integer('Call'),
    }
sale_order_line()
