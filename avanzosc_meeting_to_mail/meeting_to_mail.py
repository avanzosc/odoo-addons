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
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time

from osv import osv, fields
from tools.translate import _

class meeting_mail(osv.osv):
    
    _name = 'meeting.mail'
    _description = 'Meeting list'
    _columns = {
                'ref':fields.char('Ref.', size=64, required=True,  states={'sent': [('readonly', True)]}),
                'installer':fields.many2one('res.users', 'Installer', required=True), 
                'meetings':fields.many2many('crm.meeting','meeting_to_mail', 'mail_id', 'id', 'Meetings'),
                'state':fields.selection([('draft', 'Draft'),('sent', 'Sent')], 'State', readonly=True),
                'start_date': fields.date('Create date'),
                'sent_date':fields.date('Sent date'),
                }
    _defaults = {
                 'start_date':lambda *a : time.strftime('%Y-%m-%d'),
                 'state':lambda *a : 'draft',
                 'ref': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'meeting.mail'),
                 }
    
    
    def set_sent(self, cr, uid, ids, context=None):
        if ids:
            mail = self.browse(cr,uid,ids[0])
            if mail.meetings:
                for meet in mail.meetings:
                    self.pool.get('crm.meeting').write(cr,uid,meet.id, {'state':'released'})
            self.write(cr, uid, ids[0], {'state':'sent', 'sent_date':time.strftime('%Y-%m-%d')})
        return True
meeting_mail()

#
class crm_meeting(osv.osv):
    
    _inherit = 'crm.meeting'
    _columns = {
                'mails': fields.many2many('meeting.mail', 'meeting_to_mail', 'id', 'mail_id', 'Mails'),
                }
crm_meeting()