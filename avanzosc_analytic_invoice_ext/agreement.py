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

from osv import fields,osv
import netsvc
import tools
import re
from tools.translate import _
from mx import DateTime
from mx.DateTime import now
import time, locale
import traceback, sys


class agreement(osv.osv):
    _inherit = "inv.agreement"
    
    def set_done(self, cr, uid, ids, context={}):
        for r in self.browse(cr, uid, ids, {}):
            self.pool.get('ir.cron').write(cr, uid, r.cron_id.id, {'active':False})
            
            inv_type = self.pool.get('hr_timesheet_invoice.factor').search(cr,uid,[('canceled','=',True)])[0]
            for line in r.analytic_entries:
                if not line.invoice_id:
                    self.pool.get('account.analytic.line').write(cr,uid,line.id,{'to_invoice':inv_type})
        self.write(cr, uid, ids, {'state':'done'})
        return True
    
agreement()