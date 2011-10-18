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

    def create(self, cr, uid, vals, context={}):
	if 'cron_id' in vals.keys():
            self.pool.get('ir.cron').unlink(cr,uid,[vals['cron_id']])
            del vals['cron_id']
	if 'cron_nextdate' in vals.keys():
            self.pool.get('ir.cron').unlink(cr,uid,[vals['cron_nextdate']])
            del vals['cron_nextdate']
        result = super(agreement, self).create(cr, uid, vals, context)
        return result

    
    def write(self, cr, uid, ids, vals, context=None):
	if 'cron_id' in vals.keys():
            self.pool.get('ir.cron').unlink(cr,uid,[vals['cron_id']])
            del vals['cron_id']
	if 'cron_nextdate' in vals.keys():
            self.pool.get('ir.cron').unlink(cr,uid,[vals['cron_nextdate']])
            del vals['cron_nextdate']
        
        return super(agreement, self).write(cr, uid, ids, vals, context=context)
    
agreement()
