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
from crm import crm
from osv import fields, osv
from tools.translate import _

class training_course(osv.osv):
    _inherit = 'training.course'
    
    _columns = {
	    'course_code': fields.char('Course Code', size=32, required=True),
        'product_id':fields.many2one('product.product', 'Product'),
#        'tipo_docencia':fields.selection([('F', 'F'),('L', 'L'),('N', 'N'),('X', 'X')], 'Type teaching', required=True),
		'credits': fields.float('Credits', required=True, digits=(2,1), help="Course credits"),	
		'offer_ids' : fields.one2many('training.course.offer.rel', 'course_id', 'Offers', help='A course could be included on some offers'),
		'seance_ids' : fields.one2many('training.seance', 'course_id', 'Offers', help='A course could generate some seances'),
        
    }

training_course()

class training_course_offer_rel(osv.osv):
    _inherit = 'training.course.offer.rel'
    
    def _func_name(self, cr, uid, ids, field_name, arg, context=None):
        res={}
        record_list = self.browse(cr,uid,ids)
        for rec in record_list:            
            name =rec.course_id.name
            res[rec.id] = name
        return res
    
    _columns = {
       'name': fields.function(_func_name, method=True, string='Name', size=128,type = 'char'),
       'tipology': fields.selection([
                ('basic', 'Basic'),
                ('mandatory', 'Mandatory'),
                ('optional', 'Optional'),
                ('freechoice','Free Choice'),
                ('trunk', 'Trunk'),
                ('degreework','Degree Work'),   
          ], 'Tipology', required=True),
     }
#    def name_get(self, cr, uid, ids, context=None):
#        res=[]
#        reads = self.read(cr, uid, ids, ['matching','name'], context=context)
#        for record in reads:
#            data=[]
#            name=""
#            if record['name']:
#                if record['name']:
#                    name = record['name']
#                    data.insert(0, name)
#            if record['id']:
#                res.append((record['id'],name))
#        return res
training_course_offer_rel()

class training_session(osv.osv):
    _inherit = 'training.session'

    _columns = {
        'date_from' : fields.datetime('Date From', required=True, help="The data when course begins"),
        'date_end' : fields.datetime('Date End', required=True, help="The data when course ends"),   
     }

training_session()

class training_seance(osv.osv):
    _inherit = 'training.seance'
    
    def onchange_course_id(self, cr, uid, ids, course_id, context=None):
        #OBJETOS
        ##########################################################
        training_course_obj = self.pool.get('training.course')
        ##########################################################
        res = {}
        if course_id:
           val = training_course_obj.browse(cr, uid, course_id, context=None).credits
           res = {'credits': val}
        return {'value': res}

    _columns = {
        'date_from' : fields.datetime('Date From', required=True, help="The data when course begins"),
        'offer_id':fields.many2one('training.offer','Offer',required = True),
        'date_to' : fields.datetime('Date To', required=True, help="The data when course ends"),
        'coursenum_id' : fields.many2one('training.coursenum', 'Number Course'),
        'credits': fields.float('Credits', required=True, readonly=True, help="Course credits"), 
        'semester': fields.selection([('first_semester','First Semester'),('second_semester','Second Semester'),('all_year','All Year')],'Semester',required=True),
        'tipology': fields.selection([                            
                ('basic', 'Basic'),
                ('mandatory', 'Mandatory'),
                ('optional', 'Optional'),
                ('freechoice','Free Choice'),
                ('trunk','Trunk'),
                ('degreework','Degree Work'),
        ], 'Tipology',required=True),
     }
training_seance()



