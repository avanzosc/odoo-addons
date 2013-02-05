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

from datetime import datetime
from dateutil.relativedelta import relativedelta
import time
from operator import itemgetter
from itertools import groupby

from osv import fields, osv
from tools.translate import _
import netsvc
import tools
import decimal_precision as dp
import logging

class stock_move(osv.osv):
    
    _name="stock.move"
    _inherit="stock.move"
    
    _columns={
              'is_recession':fields.boolean('Is Recession'),
              }
    
    def action_done(self, cr, uid, ids, context=None):
        lot_obj = self.pool.get('stock.production.lot')
        res = super(stock_move, self).action_done(cr, uid, ids, context=context)
        for m_id in ids:
            m_o = self.browse(cr,uid,m_id)
	    if m_o.is_recession:
		if m_o.prodlot_id:
		   lot_obj.write(cr,uid,[m_o.prodlot_id.id], {'customer':False, 'cust_address':False, 'installer':False, 'technician':False})
		   lot_obj.action_nouse(cr,uid,[m_o.prodlot_id.id])
        return res
stock_move()
