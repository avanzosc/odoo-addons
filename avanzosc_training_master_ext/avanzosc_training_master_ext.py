
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


class titles(osv.osv):
    _name='titles'
    _description='titles'
    _columns = {
            'title_id':fields.char('Code',size=64),
            'name':fields.char('Name',size=64),
    }
titles()

class source(osv.osv):
    _name='source'
    _description='source'
    _columns = {
            'code':fields.char('Reference',size=64),
            'name':fields.char('Name',size=64),
    }
source()


class universities(osv.osv):
    _name='universities'
    _description='universities'
    _columns = {
            'code':fields.char('Reference',size=64),
            'name':fields.char('Name',size=64),
    }
universities()



class training_offer(osv.osv):
    _inherit = 'training.offer'
    _columns = {
            'active': fields.boolean('Activo'),
            'numhours': fields.integer('Num.Horas',size=2),
            'letter': fields.char('Letra', size=64),
            'shortname': fields.char('Nombre corto', size=64),
            'numcursos': fields.integer('Num Cursos'), 
            'impcredito': fields.integer('Imp Credito'),
            'gradoexp': fields.integer('Grado Exp'),
            'title_id': fields.many2one('titles','Title'),
			'title_id2': fields.many2one('titles','Title Additional'),
            'boe': fields.char('boe',size=64),
            'textoboe': fields.text('TextBOE',size=64),                   
    } 
    _defaults = { 'active': lambda *a : True,
	}
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

    }
    
training_course()

class training_course_offer_rel(osv.osv):
    _inherit = 'training.course.offer.rel'

    _columns = {
        'tipology': fields.selection([('mandatory', 'mandatory'),('trunk', 'trunk'),('optional', 'optional'),('free', 'free'),('complementary', 'complementary'),('replace', 'replace')], 'Tipology', required=True),
     }

training_course_offer_rel()