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
from osv import osv, fields
import decimal_precision as dp
import time

from tools.translate import _

class product_product(osv.osv):
    _inherit="product.product"
    _columns = {
                'last_manufacturing_cost':fields.float('Last manufacturing cost',  readonly=True),
                'last_manufacturing_end_date':fields.date('Last manufacturing end date',  readonly=True),
                }
product_product()


class mrp_production(osv.osv):
    _inherit = "mrp.production"
    def action_production_end(self, cr, uid, ids):
        """ Changes production state to Finish and writes finished date.
        @return: True
        """
        res = super(mrp_production, self).action_production_end(cr,uid,ids)
        for production in self.browse(cr, uid, ids):            
            self.pool.get('product.product').write(cr,uid,[production.product_id.id],({'last_manufacturing_end_date': time.strftime('%Y-%m-%d %H:%M:%S')}))
        return res

mrp_production()



class mrp_analytic_wizard(osv.osv_memory):    
    _inherit = "mrp.analytic.wizard"
    
    
    def create_analytic_structure(self, cr, uid, ids, context=None): 
        res = super(mrp_analytic_wizard, self).create_analytic_structure(cr,uid,ids,context)
        for production in self.pool.get('mrp.production').browse(cr, uid, context['active_ids']):
            analy_id=self.pool.get('account.analytic.account').search(cr,uid,[('name','like', production.name)])
            if analy_id:
                list = self.pool.get('account.analytic.account').browse(cr,uid,analy_id[0])
                if list:
                    haber = list.credit / production.product_qty
                    self.pool.get('product.product').write(cr,uid,[production.product_id.id],({'last_manufacturing_cost': haber})) 
        return res
mrp_analytic_wizard()