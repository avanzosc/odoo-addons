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



class account_invoice(osv.osv):
    _inherit='account.invoice'


    def onchange_partner_id(self, cr, uid, ids, type, partner_id,\
            date_invoice=False, payment_term=False, partner_bank_id=False, company_id=False):
        
        res = super(account_invoice, self).onchange_partner_id(cr,uid,ids,type,partner_id,date_invoice, payment_term, partner_bank_id, company_id )
        if partner_id:
            partner = self.pool.get('res.partner').browse(cr,uid,partner_id)
            if partner.property_account_position:
                pos_fisc = self.pool.get('account.fiscal.position').browse(cr,uid, partner.property_account_position.id)
                if pos_fisc.intracommunity_operations:
                    if vals.get('type') == 'out_invoice':
                        res['value']['operation_key'] = 'E'
                    else:
                        res['value']['operation_key'] = 'A'
        return res
    
account_invoice()