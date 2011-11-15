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
from osv import osv, fields
from tools.translate import _

class crm_meeting_responsible_change(osv.osv_memory):
    
    _name = 'crm.meeting.responsible.change'
    _description = 'Provides to change responsible for many meetings.'
    
    
    _columns = {
                'next_responsible':fields.many2one('res.users', 'Next responsible', size=16, required=True),
                }

    
    def change_responsible(self, cr, uid, ids, context=None):
        
        meeting_ids =  context.get('active_ids',[])
        responsible = self.browse(cr,uid,ids[0]).next_responsible
        if meeting_ids:
            for meeting in meeting_ids:
                self.pool.get('crm.meeting').write(cr,uid,[meeting], {'user_id':responsible.id})
        return {'type': 'ir.actions.act_window.close()'}
    
crm_meeting_responsible_change()    
