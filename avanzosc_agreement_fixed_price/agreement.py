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
    
    _columns = {
        'fixed_price':fields.float('Fixed Price', digits=(10,3))
    }
    
    def update_analytic_lines(self, cr, uid, ids, context=None):
        analytic_line_obj = self.pool.get('account.analytic.line')
        for agreement in self.browse(cr, uid, ids):
            for analytic_line in agreement.analytic_entries:
                if not analytic_line.invoice_id:
                    analytic_line_obj.write(cr, uid, [analytic_line.id], {'sale_amount': agreement.fixed_price})
        return True
    
agreement()