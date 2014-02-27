# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc - Advanced Open Source Consulting
#    Copyright (C) 2011 - 2014 Avanzosc <http://www.avanzosc.com>
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
from datetime import datetime

class payment_order(osv.osv):
    
    _inherit = 'payment.order'
    _columns = {
                'incurrent_payment':fields.boolean('Incurrent Payment')
                }
    def set_done(self, cr, uid, ids, context=None):
        
        invoice_obj = self.pool.get('account.invoice')
        payment_line_obj = self.pool.get('payment.line')
        
        
        result = super(payment_order, self).set_done(cr, uid, ids, context)
        for id in ids:
            inv_list = []
            line_ids = self.read(cr,uid,id,['incurrent_payment','line_ids'],context)
            if line_ids['incurrent_payment']:
                for line_id in line_ids['line_ids']:
                    inv = payment_line_obj.read(cr,uid,line_id,['ml_inv_ref'])
                    inv_list.append(inv['ml_inv_ref'][0])
                if inv_list:
                    invoice_obj.write(cr,uid,inv_list, {'last_relaunch_date':datetime.now()})    
        return result
payment_order()