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

class wiz_create_record_lines(osv.osv_memory):
    _name = 'wiz.create.record.lines'
    _description = 'Wizard to Create Record Lines'
    
    def create_record_lines(self, cr, uid, ids, context=None):
        res = []
        session_obj = self.pool.get('training.record.line')
        for record in self.pool.get('training.record').browse(cr, uid, context['active_ids']):
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
        return {'type': 'ir.actions.act_window_close'}
    
wiz_create_record_lines()