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
from osv import osv
from osv import fields

class training_record(osv.osv):
    _name = 'training.record'
    _description = 'Training Record'
training_record()

class training_record_line(osv.osv):
     _name = 'training.record.line'
     _description = 'Training Record Line'

     _columns = {
         'name': fields.char('Name', size=64, readonly=True ,states={'close': [('readonly', True)]}),
         'seance_id': fields.many2one('training.seance', 'Seance', required=True, readonly=True, states={'close': [('readonly', True)]}),
         'date': fields.datetime('Date', required=True ,states={'close': [('readonly', True)]}),
         'credits': fields.integer('Credits', required=True, help="Course credits" ,states={'close': [('readonly', True)]}),
         'tipology': fields.selection([
                ('basic', 'Basic'),
                ('mandatory', 'Mandatory'),
                ('optional', 'Optional'),
                ('trunk', 'Trunk'),
                ('degreework','Degree Work'),   
          ],'Tipology', required=True, states={'close': [('readonly', True)]}),
         'call': fields.integer('Call', states={'close': [('readonly', True)]}),
         'mark': fields.float('Mark', states={'close': [('readonly', True)]}),
         'state': fields.selection([
             ('passed', 'Passed'),
             ('failed', 'Failed'),
             ('not_sub', 'Not Submitted'),
             ('recognized', 'Recognized'),
             ('noassistance','No Assistance'),
             ('no_used','No Used'),
         ],'State', required=True, states={'close': [('readonly', True)]}),
         'type': fields.selection([
             ('ordinary','Ordinary'),
             ('extraordinary','Extraordinary'),
         ],'Type', required=True, states={'close': [('readonly', True)]}),
         'record_id': fields.many2one('training.record', 'Record', required=True, states={'close': [('readonly', True)]}),
         'type':fields.selection([('ordinary', 'Ordinary'),('extraordinary', 'Extraordinary')],'Type',required=True, states={'close': [('readonly', True)]}),
         'coursenum_id' : fields.many2one('training.coursenum','Number Course', states={'close': [('readonly', True)]}),
         'checkrec': fields.boolean('CheckRec', states={'close': [('readonly', True)]}),
         
        
     }

     _defaults = {
         'state': lambda *a: 'not_sub',
     }

     def onchange_mark(self, cr, uid, ids, mark, context=None):
         res = {}
         if mark >= 5:
             res = {
                 'state': 'passed',
             }
         elif mark < 5:
             res = {
                 'state': 'failed',
             }
         return {'value': res}

training_record_line()

class training_record(osv.osv):
    #Urtzi
    _inherit = 'training.record'
    
    def _calculate_credits(self, cr, uid, ids, field_name, arg, context={}):
        '''   
         Calculos de los creditos aprobados divididos por categorias: Trunk,
         Mandatory, Optional, Basic 
        '''
        
        res = {}
        for record in self.browse(cr, uid, ids):
            sum_total = 0
            res[record.id] = {
                'total_cycle': 0,
                'curr_basic': 0,
                'curr_mandatory': 0,
                'curr_optional': 0,
                'curr_degree': 0,
                'curr_total': 0,
                'curr_trunk': 0,
                'progress_rate': 0,
            }
            sum_total += record.basic_cycle
            sum_total += record.mandatory_cycle
            sum_total += record.optional_cycle
            sum_total += record.trunk_cycle
            sum_total += record.degree_cycle
            res[record.id]['total_cycle'] = sum_total
            
            sum_basic = 0
            sum_mandatory = 0
            sum_optional = 0
            sum_degree = 0
            sum_trunk = 0
            sum_curr = 0
            
            for line in record.record_line_ids:
                if line.state in ('passed', 'recognized'):
                    if line.tipology == 'basic':
                        sum_basic += line.credits
                        sum_curr += line.credits
                    elif line.tipology == 'mandatory':
                        sum_mandatory += line.credits
                        sum_curr += line.credits
                    elif line.tipology == 'optional':
                        sum_optional += line.credits
                        sum_curr += line.credits
                    elif line.tipology == 'degreework':
                        sum_degree += line.credits
                        sum_curr += line.credits
                    elif line.tipology == 'trunk':
                        sum_trunk += line.credits
                        sum_curr += line.credits
            res[record.id]['curr_basic'] = sum_basic
            res[record.id]['curr_mandatory'] = sum_mandatory
            res[record.id]['curr_optional'] = sum_optional
            res[record.id]['curr_trunk'] = sum_trunk
            res[record.id]['curr_degree'] = sum_degree
            res[record.id]['curr_total'] = sum_curr
        return res
    
    def _record_rate(self, cr, uid, ids, field_name, arg, context={}):
        '''   
         Calculos de la barre de progreso de aprobados.  
        '''
        res = {}
        for record in self.browse(cr, uid, ids):
            if record.curr_total > 0 and record.total_cycle > 0:
                res[record.id] = (float(record.curr_total) * 100) / float(record.total_cycle)
            else:
                res[record.id] = 0
        return res
 
    _columns = {
        'name':fields.char('Record Nº', size=64, required=True, states={'close': [('readonly', True)]}),
        'graduate_data':fields.date('Graduate data', states={'close': [('readonly', True)]}),
        'student_id': fields.many2one('res.partner.contact', 'Student',required=True, states={'close': [('readonly', True)]} ),
        'offer_id': fields.many2one('training.offer', 'Offer', required=True, states={'close': [('readonly', True)]}),
        'edition_ids': fields.many2many('training.session','training_record_edition_rel','edition_id', 'record_id', 'Edition List', states={'close': [('readonly', True)]}),
        'note': fields.text('Notes', states={'close': [('readonly', True)]}),
        'basic_cycle': fields.integer('Basic', states={'close': [('readonly', True)]}),
        'mandatory_cycle': fields.integer('Mandatory', states={'close': [('readonly', True)]}),
        'optional_cycle': fields.integer('Optional', states={'close': [('readonly', True)]}),
        'degree_cycle': fields.integer('Degree Work', states={'close': [('readonly', True)]}),
        'trunk_cycle': fields.integer('Trunk', states={'close': [('readonly', True)]}),
        'total_cycle': fields.function(_calculate_credits, method=True, type='integer', string='Total Credits', store=True, multi='sum'),
        'curr_basic': fields.function(_calculate_credits, method=True, type='integer', string='Current Basic', store=True,multi='sum'),
        'curr_mandatory': fields.function(_calculate_credits, method=True, type='integer', string='Current Mandatory', store=True, multi='sum'),
        'curr_optional': fields.function(_calculate_credits, method=True, type='integer', string='Current Optional', store=True, multi='sum'),
        'curr_degree': fields.function(_calculate_credits, method=True, type='integer', string='Current Degree', store=True, multi='sum'),
        'curr_trunk': fields.function(_calculate_credits, method=True, type='integer', string='Current Trunk', store=True, multi='sum'),
        'curr_total': fields.function(_calculate_credits, method=True, type='integer', string='Current Total', store=True, multi='sum'),
        'record_line_ids': fields.one2many('training.record.line', 'record_id', 'Record Lines', states={'close': [('readonly', True)]}),
        'progress_rate': fields.function(_record_rate, method=True, string='Progress (%)', type='float', states={'close': [('readonly', True)]}),
        'state': fields.selection([
               ('open','Opened'),
               ('close','Closed'),
        ],'State', readonly=True),
    }
    
    _defaults = {
        'name': lambda self,cr,uid,context={}: self.pool.get('ir.sequence').get(cr, uid, 'training.record'),
        'state':lambda *a:'open',
    }
    
    def onchange_offer(self, cr, uid, ids, offer_id, context=None):
        res = {}
        if offer_id:
            offer = self.pool.get('training.offer').browse(cr, uid, offer_id)
            res = {
                'basic_cycle': offer.basic_cycle or 0,
                'mandatory_cycle': offer.mandatory_cycle or 0,
                'trunk_cycle': offer.trunk_cycle or 0,
                'optional_cycle': offer.optional_cycle or 0,
                'degree_cycle': offer.degree_cycle or 0,
            }
        return {'value': res }
    
    def button_dummy(self, cr, uid, ids, context=None):
        return True
    
    #######################################################
    ## METODOS DEL WORKFLOW ##
    #######################################################

    def action_open(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'open'})
        return True
    
    def action_close(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'close'})
        return True  
    
training_record()
