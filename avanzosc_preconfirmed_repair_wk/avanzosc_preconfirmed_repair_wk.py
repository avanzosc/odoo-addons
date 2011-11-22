
# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2004-2010 Tiny SPRL (http://tiny.be). All Rights Reserved
#    
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

from osv import fields,osv
import netsvc
from datetime import datetime
from dateutil.relativedelta import relativedelta
from tools.translate import _
import decimal_precision as dp

class mrp_repair(osv.osv):
    
    _inherit = 'mrp.repair'
    _columns = {
        'state': fields.selection([
            ('draft','Quotation'),
            ('preconfirmed','Pre-confirmed'),
            ('confirmed','Confirmed'),
            ('ready','Ready to Repair'),
            ('under_repair','Under Repair'),
            ('2binvoiced','To be Invoiced'),
            ('invoice_except','Invoice Exception'),
            ('done','Done'),
            ('cancel','Cancel')
            ], 'State', readonly=True,
            help=' * The \'Draft\' state is used when a user is encoding a new and unconfirmed repair order. \
            \n* The \'Pre-confirmed\' state is used when a user preconfirm the repair order. \
            \n* The \'Confirmed\' state is used when a user confirms the repair order. \
            \n* The \'Ready to Repair\' state is used to start to repairing, user can start repairing only after repair order is confirmed. \
            \n* The \'To be Invoiced\' state is used to generate the invoice before or after repairing done. \
            \n* The \'Done\' state is set when repairing is completed.\
            \n* The \'Cancelled\' state is used when user cancel repair order.'),        
                }
    
    def action_preconfirm(self, cr, uid, ids, *args):
        """ We repair order to state "pre-confirmed" before moving on to "confirmed".
        @param *arg: Arguments
        @return: True
        """
        
        for o in self.browse(cr, uid, ids):
            self.write(cr, uid, [o.id], {'state': 'preconfirmed'})
        return True
    
    def action_preconfirmed_to_draft(self, cr, uid, ids, *args):
        """ The repair order status passes "draft".
        @param *arg: Arguments
        @return: True
        """
        
        if not len(ids):
            return False
        mrp_line_obj = self.pool.get('mrp.repair.line')
        for repair in self.browse(cr, uid, ids):
            mrp_line_obj.write(cr, uid, [l.id for l in repair.operations], {'state': 'draft'})
        self.write(cr, uid, ids, {'state':'draft'})
        wf_service = netsvc.LocalService("workflow")
        for id in ids:
            wf_service.trg_create(uid, 'mrp.repair', id, cr)
        return True
    
    
    
mrp_repair()