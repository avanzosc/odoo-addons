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

import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from operator import itemgetter

import netsvc
import pooler
from osv import fields, osv
import decimal_precision as dp
from tools.translate import _

class account_move(osv.osv):
    
    _name="account.move"
    _inherit="account.move"
    
    def set_partner_on_lines(self, cr, uid, ids, context=None):
        move_obj=self.pool.get('account.move')
        property_obj = self.pool.get('ir.property')
        for move in ids:
            
            move_o = move_obj.browse(cr,uid,move)
            for line in move_o.line_id:
                partner_id = False
                partner_list = property_obj.search(cr,uid,[('name','=','property_account_receivable'),('res_id','!=',False),('value_reference','=','account.account,'+str(line.account_id.id)+'')])
                if partner_list and not line.partner_id:
                    if len(partner_list) == 1:
                        partner_list_o = property_obj.browse(cr,uid, partner_list[0])
                        partner_id = partner_list_o.res_id.id
                        cr.execute('update account_move_line set partner_id=%s where id=%s', (partner_id, line.id))
                        cr.commit()
                        
                if not partner_id:
                    partner_list = property_obj.search(cr,uid,[('name','=','property_account_payable'),('res_id','!=',False),('value_reference','=','account.account,'+str(line.account_id.id)+'')])
                    if partner_list and not line.partner_id:
                        if len(partner_list) == 1:
                            partner_list_o = property_obj.browse(cr,uid, partner_list[0])
                            partner_id = partner_list_o.res_id.id
                            cr.execute('update account_move_line set partner_id=%s where id=%s', (partner_id, line.id))
                            cr.commit()
                            
        return True
account_move()
    