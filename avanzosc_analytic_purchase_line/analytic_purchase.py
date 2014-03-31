
# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2008-2013 AvanzOSC (Daniel). All Rights Reserved
#    Date: 13/11/2013
#    
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
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

from osv import osv, fields
import netsvc
from tools.translate import _

class purchase_order(osv.osv): 

    _description = 'purchase order Inheritance'
    _inherit = 'purchase.order'
    
    _columns = {
                'analytic_account' : fields.many2one('account.analytic.account', 'Analytic Account'),
                }
    
    def purchase_confirm(self, cr, uid, ids, context):
        wf_service = netsvc.LocalService("workflow")
        if isinstance(ids,int):
            ids = [ids]
        res = {}
        purchase_line_obj = self.pool.get('purchase.order.line')
        purchase_order = self.browse(cr, uid, ids[0], context=context)
        purchase_lines_lst = purchase_line_obj.search(cr,uid,[('order_id','=',ids[0])])
        for pline_id in purchase_lines_lst:
            purchase_line = purchase_line_obj.browse(cr,uid,pline_id)
            if not purchase_line.account_analytic_id:
                if not purchase_order.analytic_account:
                    raise osv.except_osv(_('Error!'),_('Purchase order has no analytic account assigned!'))
                else:
                    purchase_line_obj.write(cr,uid,pline_id,{
                                                             'account_analytic_id': purchase_order.analytic_account.id
                                                             })
        res = wf_service.trg_validate(uid, 'purchase.order', ids[0], 'purchase_confirm', cr)
        return res
    
purchase_order()
