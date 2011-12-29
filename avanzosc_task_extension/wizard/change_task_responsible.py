# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc - Avanced Open Source Consulting
#    Copyright (C) 2010 - 2011 Avanzosc <http://www.avanzosc.com>
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
from osv import osv, fields
from tools.translate import _

class task_responsible_change(osv.osv_memory):
    
    _name = 'task.responsible.change'
    _description = 'Provides to change responsible for many tasks.'
    
    
    _columns = {
                'responsible':fields.many2one('res.users', 'Responsible', size=16, required=True),
                'limit_date':fields.date('Limit date', required=True),
                }

    
    def change_responsible(self, cr, uid, ids, context=None):
        
        task_ids =  context.get('active_ids',[])
        responsible = self.browse(cr,uid,ids[0]).responsible
        date = self.browse(cr,uid,ids[0]).limit_date
        if task_ids:
            for task in task_ids:
                self.pool.get('project.task').write(cr,uid,[task], {'user_id':responsible.id, 'date_deadline':date})
        return {'type': 'ir.actions.act_window.close()'}
    
task_responsible_change()    