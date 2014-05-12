
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
from tools.translate import _
import netsvc

class sale_order(osv.osv): 

    _inherit = 'sale.order'
    
    def copy(self, cr, uid, id, default=None, context=None):
        if not default:
            default = {}
        default.update({
            'state': 'draft',
            'shipped': False,
            'invoice_ids': [],
            'picking_ids': [],
            'date_confirm': False,
            'name': '/copy',
        })
        return super(osv.osv, self).copy(cr, uid, id, default, context=context)
    
    def write(self, cr, uid, ids, vals, context=None):
        if ids:
            for sale in self.browse(cr,uid,ids,context=context):
                if sale.name == '/copy':
                    vals.update({'name': self.pool.get('ir.sequence').get(cr, uid, 'sale.order')})

        return super(sale_order, self).write(cr, uid, ids, vals, context=context)
    
sale_order()