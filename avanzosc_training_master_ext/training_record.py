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
        'name': fields.char('Name', size=64, readonly=True),
        'session_id': fields.many2one('training.seance', 'Session', required=True, readonly=True),
        'date': fields.datetime('Date', required=True),
        'call': fields.integer('Call'),
        'mark': fields.float('Mark'),
        'submitted': fields.selection([
            ('nothing','--'),
            ('sub','Submitted'),
            ('not_sub','Not Submitted'),
        ], 'Submitted', required=True),
        'state': fields.selection([
            ('nothing','--'),                      
            ('passed','Passed'),
            ('failed','Failed'),
            ('recognized','Recognized'),
        ], 'State', required=True),
        'record_id': fields.many2one('training.record', 'Record', required=True),
    }
    
#    def onchange_session(self, cr, uid, ids, session_id, context=None):
#        res = {}
#        if session_id:
#            session = self.pool.get('training.seance').browse(cr, uid, session_id)
#            res = {
#                'name': session.name,
#            }
#        return {'value': res}
    
training_record_line()

class training_record(osv.osv):
    _inherit = 'training.record'
 
    _columns = {
        'number':fields.char('Record Nº', size=64, required=True),
        'student_id': fields.many2one('res.partner.contact', 'Student',required=True ),
        'offer_id': fields.many2one('training.offer', 'Offer', required=True),
        'title_id': fields.many2one('training.titles', 'Title', required=True),
        'edition_ids': fields.many2many('training.session','training_record_edition_rel','edition_id', 'record_id', 'Edition List'),
        'note': fields.text('Notes'),
        'record_line_ids': fields.one2many('training.record.line', 'record_id', 'Record Lines'), 
    }
    
    _defaults = {
        'number': lambda self,cr,uid,context={}: self.pool.get('ir.sequence').get(cr, uid, 'training.record'),
    }
    
    def onchange_offer(self, cr, uid, ids, offer_id, context=None):
        res = {}
        if offer_id:
            offer = self.pool.get('training.offer').browse(cr, uid, offer_id)
            res = {
                'title_id': offer.title_id.id,
            }
        return {'value': res}
    
    def create_record_lines(self, cr, uid, ids, context=None):
        res = []
        session_obj = self.pool.get('training.record.line')
        for record in self.browse(cr, uid, ids):
            for edition in record.edition_ids:
                if edition.state == 'inprogress':
                    for session in edition.seance_ids:
                        values = {
                            'name': session.name,
                            'session_id': session.id,
                            'date': time.strftime('%Y-%m-%d %H:%M:%S'),
                            'submitted': 'sub',
                            'record_id': record.id,
                        }
                        session_id = session_obj.create(cr, uid, values)
                        res.append(session_id)
        return res
    
training_record()
