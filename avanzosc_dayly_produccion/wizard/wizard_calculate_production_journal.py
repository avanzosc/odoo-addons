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

class calculate_production_journal(osv.osv_memory):
    
    _name="calculate.production.journal"
    _columns={
              'start_date':fields.date('Start date', required=True),
              'end_date': fields.date('End date', required=True)
              }
    def calculate_data(self,cr,uid,ids,context=None):
        start = datetime.strptime(time.strftime('%Y-%m-%d'), "%Y-%m-%d")
        end = datetime.strptime(time.strftime('%Y-%m-%d'), "%Y-%m-%d")
        for wizard in self.browse(cr,uid,ids,context):
            start = wizard.start_date
            end = wizard.end_date
        self.pool.get('dayly.production').calc_data(cr, uid, ids, start, end,context)
        return {'type': 'ir.actions.act_window.close()'}
calculate_production_journal()