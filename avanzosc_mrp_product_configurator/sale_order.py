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

from osv import osv
from osv import fields

class sale_order(osv.osv):

    _inherit = 'sale.order'
 
    _columns = {
            'configure':fields.boolean('Configure', size=64, readonly=True),
    }
    
    def action_wait(self, cr, uid, ids, *args):
        bom_obj = self.pool.get('mrp.bom')
        configure = False
        for o in self.browse(cr, uid, ids):
            for line in o.order_line:
                bom_id = bom_obj.search(cr, uid, [('product_id', '=', line.product_id.id)])
                for bom in bom_obj.browse(cr, uid, bom_id):
                    for bom_line in bom.bom_lines:
                        if bom_line.product_id.alt_product_ids:
                            configure = True
            if configure:
                self.write(cr, uid, [o.id], {'configure': configure})
        super(sale_order, self).action_wait(cr, uid, ids)    
        return True
    
sale_order()