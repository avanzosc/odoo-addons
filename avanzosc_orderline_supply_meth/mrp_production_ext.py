
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

class mrp_production(osv.osv): 

    _inherit = 'mrp.production'
    
    def test_if_product(self, cr, uid, ids):
        """
        @return: True or False
        """
        res = True
        for production in self.browse(cr, uid, ids):
            if not production.product_lines:
                res = False

        return res
    
    def action_confirm(self, cr, uid, ids):
        product_obj = self.pool.get('product.product')

        for production in self.browse(cr, uid, ids):
            if not production.product_lines:
                raise osv.except_osv(_('Confirm Production ERROR'), _('No scheduled products defined') )
            else:
                for line in production.product_lines:
                    if line.supply_method not in ('produce','buy'):
                        raise osv.except_osv(_('Confirm Production ERROR'), _('You must define PRODUCE OR BUY for product: %s') %(line.product_id.name))
                    else:
                        if line.buy_produce:
                            product_obj.write(cr,uid,[line.product_id.id],{'supply_method': line.supply_method})
                            
        result = super(mrp_production,self).action_confirm(cr,uid,ids)
        
        for production in self.browse(cr, uid, ids):
            for line in production.product_lines:
                if line.buy_produce:
                    product_obj.write(cr,uid,[line.product_id.id],{'supply_method': 'buy/produce'})        
        
        return result
    
mrp_production()