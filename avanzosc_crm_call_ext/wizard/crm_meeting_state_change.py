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

class crm_meeting_state_change(osv.osv_memory):
    
    _name = 'crm.meeting.state.change'
    _description = 'Provides to change state for many meetings.'
    
    def view_init(self, cr, uid, fields, context=None):
        
        if context is None:
            context={}

        meeting_ids =  context.get('active_ids',[])
        if meeting_ids:
            meetings = self.pool.get('crm.meeting').browse(cr,uid,meeting_ids)
            state = meetings[0].state
            for meeting in meetings:
                if (meeting.state != state ):
                    raise osv.except_osv(_('Error!'), _('All meetings should have the same state.'))
        return False
    
    def _get_selection(self, cr, uid,context=None):
        if context is None:
            context={}
        res=[]
        meeting_ids =  context.get('active_ids',[])
        if meeting_ids:
            meetings = self.pool.get('crm.meeting').browse(cr,uid,meeting_ids)
            state = meetings[0].state
            if state=='draft':
                res=[('open', 'Confirmed')]
            elif state=='open':
                res=[('done', 'Done'),('released', 'Released'), ('draft', 'Unconfirmed')]
            elif state=='cancel':    
                res=[('draft', 'Unconfirmed')]
            elif state=='done':
                res=[('draft', 'Unconfirmed')]
            elif state=='released':
                res=[('done', 'Done'),('draft','Unconfirmed')]
        return res
    
    _columns = {
                'next_state':fields.selection(_get_selection, 'Next state', size=16, required=True),
                }

    
    def change_state(self, cr, uid, ids, context=None):
        
        meeting_ids =  context.get('active_ids',[])
        state = self.browse(cr,uid,ids[0]).next_state
        if meeting_ids:
            for meeting in meeting_ids:
                self.pool.get('crm.meeting').write(cr,uid,[meeting], {'state':state})
        return {'type': 'ir.actions.act_window.close()'}
    
crm_meeting_state_change()    
