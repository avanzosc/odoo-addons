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

class wiz_delete_record_lines(osv.osv_memory):
    _name = 'wiz.delete.record.lines'
    _description = 'Wizard Delete Record Lines'
    
    def delete_lines(self, cr, uid, ids, context={}):
        for record in self.pool.get('training.record').browse(cr, uid, context['active_ids']):
            for line in record.record_line_ids:
                if line.state == 'no_used':
                    self.pool.get('training.record.line').unlink(cr, uid, [line.id])
        return {'type': 'ir.actions.act_window_close'}
    
wiz_delete_record_lines()