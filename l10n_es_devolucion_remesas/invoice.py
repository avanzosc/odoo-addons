# -*- encoding: utf-8 -*-
##############################################################################
#
#    7 i TRIA
#    Copyright (C) 2011 - 2012 7 i TRIA <http://www.7itria.cat>
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
from lxml import etree
import decimal_precision as dp

import netsvc
import pooler
from osv import fields, osv, orm
from tools.translate import _


#class account_move(osv.osv):
#    
#    _inherit='account.move'
#    _columns = {
#                'ret_inv':fields.many2one('account.invoice', 'Return invoice'),
#                }
#account_move()

class account_invoice(osv.osv):
    
    _inherit = 'account.invoice'
    
    _columns = {'state': fields.selection([
            ('draft','Draft'),
            ('proforma','Pro-forma'),
            ('proforma2','Pro-forma'),
            ('open','Open'),
            ('paid','Paid'),
            ('unpaid','Unpaid'),
            ('cancel','Cancelled')
            ],'State', select=True, readonly=True,
            help=' * The \'Draft\' state is used when a user is encoding a new and unconfirmed Invoice. \
            \n* The \'Pro-forma\' when invoice is in Pro-forma state,invoice does not have an invoice number. \
            \n* The \'Open\' state is used when user create invoice,a invoice number is generated.Its in open state till user does not pay invoice. \
            \n* The \'Paid\' state is set automatically when invoice is paid.\
            \n* The \'Cancelled\' state is used when user cancel invoice.'), 
            }

    def test_paid2(self, cr, uid, ids, *args):
        res = False
        if ids:
            inv = self.browse(cr, uid, ids[0])
            residual = inv._amount_residual
            if residual == 0.0:
                res = True
        return res
    def action_unpaid(self, cr, uid, ids, *args):
        res = False
        for id in ids:
            wf_service = netsvc.LocalService("workflow")
            wf_service.trg_validate(uid, 'account.invoice', id, 'open_test2', cr)
            res = True
        return res
account_invoice()
    
