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
import decimal_precision as dp

class training_credit_prices(osv.osv):
    '''
    Objeto de precios de titulos simples
    '''
    _name = 'training.credit.prices'
    _description = 'credit prices'
    
    _columns = {
            'num_comb': fields.integer('Num.Combo'),
            'price_credit': fields.float('Price per Credit', digits_compute=dp.get_precision('Account')),
            'price_credit_teaching': fields.float('Price per Credit (Teaching)', digits_compute=dp.get_precision('Account')),
            }
training_credit_prices()

class training_credit_super_prices(osv.osv):
    '''
    Objeto de precios de los titulos dobles
    '''
    _name = 'training.credit.super.prices'
    _description = 'credit super prices'
    
    _columns = {
        'num_comb': fields.integer('Num.Combo'),
        'price_credit_t1': fields.float('1st Price', digits_compute=dp.get_precision('Account')),
        'price_credit_teaching_t1': fields.float('1st Teaching Price', digits_compute=dp.get_precision('Account')),
        'price_credit_t2': fields.float('2nd Price', digits_compute=dp.get_precision('Account')),
        'price_credit_teaching_t2': fields.float('2nd Teaching Price', digits_compute=dp.get_precision('Account')),
    }
training_credit_super_prices()

class training_matching_list(osv.osv):
    '''
    Objeto de Asignaturas pareadas
    '''
    _name = 'training.matching.list'
    _description = 'matching list'
    
    _columns = {
        'course1_id': fields.many2one('training.course.offer.rel', 'Course'),
        'course1_code':fields.related('course1_id','code',type="char",size=64,string="Course Code"),
        'course2_id': fields.many2one('training.course.offer.rel', 'Matched Course'),
        'course2_code':fields.related('course2_id','code',type="char",size=64,string="Matched Course Code"),
    }
training_matching_list()

class training_source(osv.osv):
    _name = 'training.source'
    _description = 'source'
    _columns = {
        'code':fields.char('Reference', size=64),
        'name':fields.char('Name', size=64),
    }
training_source()

class training_coursenum(osv.osv):
    #iker
    _name = 'training.coursenum'
    _description = 'coursenum'
    _columns = {
        'code':fields.integer('Reference', size=64),
        'name':fields.char('name', size=64),
    }
training_coursenum()

class training_universities(osv.osv):
    _name = 'training.universities'
    _description = 'universities'
    _columns = {
        'code':fields.char('Reference', size=64),
        'name':fields.char('Name', size=64),
        'country':fields.many2one('res.country','Country'),
        
    }
training_universities()

class training_school(osv.osv):
    
    _inherit = "training.school"
   
    _columns = {
#       ampliamos tamaño de name que venia por defecto con size=30         
        'name': fields.char('Name', size=64, required=True, select=1),
        'ministery_code':fields.char('Name', size=64),
      
        }
    
training_school()

class training_offer_type(osv.osv):
    
    _name = "training.offer.type"
    _description = "training offer type"
    _rec_name='type'
    
    _columns = {
                
        'type': fields.char('Type', size=64),
                
        }
    
training_offer_type()

class training_offer_type_line(osv.osv):
    
    _name = "training.offer.type.line"
    _description = "training offer type lines"
    
    _columns = {
                
        'offer_type':fields.many2one('training.offer.type','Offer Type'),
        'call':fields.integer('Call'),
        'price':fields.float('Price'),
                
        }
training_offer_type_line()

class training_offer_official_title(osv.osv):
    
    _name = "training.offer.official.title"
    _description = "training offer official titles"
    
    _columns = {
                
        'code':fields.integer('Title code'),
        'cod_ense': fields.char('Cod ense', size=128),
        'name':fields.char('Title name', size=128),
                
        }
training_offer_official_title()

class training_offer(osv.osv):
    #Urtzi
    #iker 08/05/2012
    _inherit = 'training.offer'
    ##############################################################
    #Calculo de los creditos totales de las tipologias de carrera#
    ##############################################################
    def _total_credits(self, cr, uid, ids, field_name, arg, context={}):
        res = {}
        sum = 0
        for title in self.browse(cr, uid, ids):
            sum += title.basic_cycle1
            sum += title.mandatory_cycle1
            sum += title.optional_cycle1
            sum += title.freechoice_cycle1
            sum += title.basic_cycle2
            sum += title.mandatory_cycle2
            sum += title.optional_cycle2
            sum += title.freechoice_cycle2
            sum += title.degree_cycle
            res[title.id] = sum
        return res
       
    _columns = {
        'cod_evaluation': fields.char('Cod_evaluation', size=64),
        'offer_code':fields.char('Offer code', size=64),
        'offer_type':fields.many2one('training.offer.type','Offer Type'),
        'active': fields.boolean('Activo'),
        'official_title':fields.many2one('training.offer.official.title','Official title'),
        'start_year':fields.integer('Start Year'),
        'end_year':fields.integer('End Year'),
        'credits_scholarship':fields.float('Credits Scholarship'),
        'numhours': fields.integer('Num.Horas', size=2),
        'letter': fields.char('Letra', size=64),
        'shortname': fields.char('Nombre corto', size=64),
        'numcursos': fields.integer('Num Cursos'),
        'impcredito': fields.integer('Imp Credito'),
        'gradoexp': fields.integer('Grado Exp'),
        'boe': fields.char('BOE', size=64),
        'textoboe': fields.text('TextBOE', size=64),
        'sub_title1': fields.many2one('training.offer', 'Subtitle 1', domain=[('super_title', '=', False)]),
        'sub_title2': fields.many2one('training.offer', 'Subtitle 2', domain=[('super_title', '=', False)]),
        'super_title': fields.boolean('Super Title'),
        'basic_cycle1': fields.float('Basic/Trunk', digits=(2, 1)),
        'mandatory_cycle1': fields.float('Mandatory', digits=(2, 1)),
        'optional_cycle1': fields.float('Optional', digits=(2, 1)),
        'freechoice_cycle1': fields.float('Free Choice', digits=(2, 1)),
        'basic_cycle2': fields.float('Basic/Trunk', digits=(2, 1)),
        'mandatory_cycle2': fields.float('Mandatory', digits=(2, 1)),
        'optional_cycle2': fields.float('Optional', digits=(2, 1)),
        'freechoice_cycle2': fields.float('Free Choice', digits=(2, 1)),
        'degree_cycle': fields.float('Degree Work', digits=(2, 1)),
        'total_cycle': fields.function(_total_credits, method=True, type='float', string='Total Credits', store=True),
        'price_list':fields.one2many('training.credit.prices', 'offer_id', 'Prices per Credit'),
        'super_price_list':fields.one2many('training.credit.super.prices', 'offer_id', 'Prices per Credit'),
        'matching_list': fields.one2many('training.matching.list', 'offer_id', 'Matched Courses'),
#        'school_id':fields.many2one('training.school','School')
    } 
    _defaults = { 
        'active': lambda * a : True,
    }
    
    def button_dummy(self, cr, uid, ids, context=None):
        return True
    
training_offer() 

class training_offer_type(osv.osv):
    
    _inherit = "training.offer.type"
   
    _columns = {
                
        'offer_ids': fields.one2many('training.offer', 'offer_type', 'Offers'),
        'line_ids':fields.one2many('training.offer.type.line', 'offer_type', 'Offer Type lines'),
      
        }
training_offer_type()

class training_credit_prices(osv.osv):
    '''
    El precio de las titulaciones simples
    '''
    _inherit = 'training.credit.prices'
    
    _columns = {
        'offer_id': fields.many2one('training.offer', 'Offer'),
    }
training_credit_prices()

class training_credit_super_prices(osv.osv):
    '''
    El precio de las titulaciones dobles
    '''
    _inherit = 'training.credit.super.prices'
    
    _columns = {
        'offer_id': fields.many2one('training.offer', 'Offer'),
    }
training_credit_super_prices()

class training_matching_list(osv.osv):
    '''
    Herencia.
    '''
    _inherit = 'training.matching.list'
    
    _columns = {
        'offer_id': fields.many2one('training.offer', 'Offer'),
    }
training_matching_list()

class training_course(osv.osv):
    '''
    Herencia de training.course para añadirle los campos necesarios.
    '''
    _inherit = 'training.course'
   
    _columns = {
        'course_code': fields.char('Course Code', size=32, required=True),
   	    'resolution': fields.char('Resolution', size=64),
        'boe': fields.char('BOE', size=32),
        'boedate':fields.date('BOE date'),
        'subjecteng': fields.char('Asignatura Eng', size=64),
        'ects': fields.integer('ECTS'),
        'product_id':fields.many2one('product.product', 'Product'),
        'type_teaching':fields.selection([('F', 'F'), ('L', 'L'), ('N', 'N'), ('X', 'X')], 'Type teaching', required=True),
        'cycle':fields.selection([('cycle1', 'Cycle 1'), ('cycle2', 'Cycle 2')], 'Cycle'),
		'credits': fields.float('Credits', required=True, digits=(2, 1), help="Course credits"), 	
		'offer_ids' : fields.one2many('training.course.offer.rel', 'course_id', 'Offers', help='A course could be included on some offers'),
		'seance_ids' : fields.one2many('training.seance', 'course_id', 'Offers', help='A course could generate some seances'),
        'coursenum_id' : fields.many2one('training.coursenum', 'Number Course'),
        'semester': fields.selection([('first_semester', 'First Semester'), ('second_semester', 'Second Semester'), ('all_year', 'All Year')], 'Semester', required=True),
        'teacher_ids': fields.many2many('res.partner.contact', 'training_course_teacher_rel', 'course_id', 'teacher_id', 'Teachers', select=1, help="The lecturers who give the course."),
    }    
training_course()

class training_external_course(osv.osv):
    '''
    cursos externos.
    '''
    _name = 'training.external.course'
    _description = 'External courses'
    
    _columns = {
        'course_code': fields.char('Course Code', size=32, required=True),
        'name': fields.char('Name', size=64, required=True),
        'university': fields.many2one('training.universities', 'University'),
        'credits':fields.float('Credits'),
        'product_uom_id':fields.many2one('product.uom', 'Product uom',required=True),
        'tipology': fields.selection([
                ('basic', 'Basic'),
                ('mandatory', 'Mandatory'),
                ('optional', 'Optional'),
                ('freechoice','Free Choice'),
                ('complement','Training Complement'),
                ('replacement','Replacement'),
                ('degreework','Degree Work'),
                ('external_practices','External Practices'),],'Tipology', required=True),
    }    
training_external_course()

class training_course_offer_rel(osv.osv):
    '''
    Objeto que une las asignaturas con las carreras
    '''
    _inherit = 'training.course.offer.rel'

    _columns = {
        'tipology': fields.selection([
                ('basic', 'Basic/Trunk'),
                ('mandatory', 'Mandatory'),
                ('optional', 'Optional'),
                ('freechoice', 'Free Choice'),
                ('complement','Training Complement'),
                ('replacement','Replacement'),
                ('degreework','Degree Work'),
                ('external_practices','External Practices'),
                
          ], 'Tipology', required=True),
    }
training_course_offer_rel()

class training_subscription(osv.osv):
    '''
    Inscripciones. Heredado para añadirle los campos que faltan.
    '''
    _inherit = 'training.subscription'
    
    _columns = {
        'universities':fields.many2one('training.universities', 'University'),
        'source':fields.many2one('training.source', 'Source')
    }
    _defaults = {
        'name': lambda self, cr, uid, context = {}: self.pool.get('ir.sequence').get(cr, uid, 'training.suscription'),
    }
training_subscription()

class training_subscription_line(osv.osv):
    '''
    Lineas de subscripción. Heredado para añadirle los campos que faltan.
    '''
    _inherit = 'training.subscription.line'
    
    _columns = {
        'code':fields.many2one('training.coursenum', 'coursenum')
     }
training_subscription_line()
