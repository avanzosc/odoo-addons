# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc, OpenERP Professional Services   
#    Copyright (C) 2010-2011 Avanzosc S.L (http://www.avanzosc.com). All Rights Reserved
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

from osv import osv
from osv import fields

class mrp_production(osv.osv):

    _inherit = 'mrp.production'
 
    _columns = {
            'state': fields.selection([('draft','Draft'),('configure', 'Waiting to Configure'),('picking_except', 'Picking Exception'),('confirmed','Waiting Goods'),('ready','Ready to Produce'),('in_production','In Production'),('cancel','Cancelled'),('done','Done')],'State', readonly=True,
                                    help='When the production order is created the state is set to \'Draft\'.\n If the order is confirmed the state is set to \'Waiting Goods\'.\n If any exceptions are there, the state is set to \'Picking Exception\'.\
                                    \nIf the stock is available then the state is set to \'Ready to Produce\'.\n When the production gets started then the state is set to \'In Production\'.\n When the production is over, the state is set to \'Done\'.'),
    }
    
    def action_configure(self, cr, uid, ids):
        """ Sets state to configure.
        @return: True
        """
        self.write(cr, uid, ids, {'state':'configure'})
        return True
    
    def test_replacement(self, cr, uid, ids, context=None):
        replace = False
        for order in self.browse(cr, uid, ids):
            for order_line in order.product_lines:
                if not order_line.product_id.sale_ok and order_line.product_id.alt_product_ids:
                    replace = True
        return replace
    
    def action_produce(self, cr, uid, production_id, production_qty, production_mode, context=None):
        sale_obj = self.pool.get('sale.order')
        super(mrp_production, self).action_produce(cr, uid, production_id, production_qty, production_mode, context)
        order = self.browse(cr, uid, production_id)
        id = sale_obj.search(cr, uid, [('name', '=', order.origin)])
        if id:
            sale_obj.write(cr, uid, id, {'configure': False})
        return True
    
mrp_production()