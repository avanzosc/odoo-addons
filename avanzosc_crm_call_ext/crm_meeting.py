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

from osv import osv
from osv import fields

class crm_meeting(osv.osv):
    _inherit = 'crm.meeting'
 
    def onchange_team(self, cr, uid, ids, team_id, context=None):
        res = {}
        section_obj = self.pool.get('crm.case.section')
        if team_id:
            team = section_obj.browse(cr, uid, team_id)
            res = {
                'user_id': team.user_id.id,
                'organizer': team.user_id.user_email,
            }
        return {'value': res}
    
crm_meeting()