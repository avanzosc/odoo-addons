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

import time
from lxml import etree
import decimal_precision as dp

import netsvc
import pooler
from osv import fields, osv, orm
from tools.translate import _


class payment_line(osv.osv):
    _inherit='payment.line'
    
    def _get_invoiced_amount(self, cr, uid, ids, name, args, context=None):
        inv_obj = self.pool.get('account.invoice')
        res = {}
        for payment in self.browse(cr, uid, ids, context):
            res[payment.id] = 0.0
            if payment.ml_inv_ref:
                inv = inv_obj.browse(cr, uid, payment.ml_inv_ref.id)
                res[payment.id] = inv.amount_total
        return res
    
    def _get_unpayed_amount(self, cr, uid, ids, name, args, context=None):
        inv_obj = self.pool.get('account.invoice')
        res = {}
        for payment in self.browse(cr, uid, ids, context=context):
            res[payment.id] = 0.0
            if payment.ml_inv_ref:
                inv = inv_obj.browse(cr, uid, payment.ml_inv_ref.id)
                res[payment.id] = inv.residual
        return res
    
    _columns={'invoiced_amount': fields.function(_get_invoiced_amount, method=True, type='float', string ='Invoiced', store=False),
              'unpayed_amount':fields.function(_get_unpayed_amount, method=True, type='float', string ='Residual', store=False),
            }
    
    
payment_line()