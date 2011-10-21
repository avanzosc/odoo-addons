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
from tools.translate import _
from base_calendar import base_calendar


class crm_meeting(osv.osv):
    _inherit = 'crm.meeting'
    
    _columns = {
        'sale_order_id': fields.many2one('sale.order', 'Sale Order'),
        'state': fields.selection([('open', 'Confirmed'),
                                    ('draft', 'Unconfirmed'),
                                    ('cancel', 'Cancelled'),
                                    ('done', 'Done'),
                                    ('released', 'Released')], 'State', \
                                    size=16, readonly=True),
    }
 
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
    
    def case_released(self, cr, uid, ids, *args):
        """Releases Case
        @param self: The object pointer
        @param cr: the current row, from the database cursor,
        @param uid: the current user’s ID for security checks,
        @param ids: List of case Ids
        @param *args: Tuple Value for additional Params
        """
        cases = self.browse(cr, uid, ids)
        cases[0].state # to fill the browse record cache
        self._history(cr, uid, cases, _('Released'))
        self.write(cr, uid, ids, {'state': 'released'})
        #
        # We use the cache of cases to keep the old case state
        #
        self._action(cr, uid, cases, 'released')
        return True
    
crm_meeting()