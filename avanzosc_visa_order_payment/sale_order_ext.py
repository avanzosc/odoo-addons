# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc - Advanced Open Source Consulting
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
    _name = 'sale.order'
    _inherit = 'sale.order'
    
    _columns = {
                'visa_pay':fields.boolean('Visa Payment'),
                }
sale_order()

class sale_order_line(osv.osv):
    _name = 'sale.order.line'
    _inherit = 'sale.order.line'
    
    def _calc_is_visa(self, cr, uid, ids, field_name, arg, context={}):
        res = {}
        for id in ids:
            val = False
            line_o = self.browse(cr,uid,id)
            if line_o.product_id and line_o.order_id:
                if line_o.product_id.visa_pay and line_o.order_id.visa_pay:
                    val = True
            res[id] = val
        return res
    
    _columns = {
                'visa_pay':fields.function(_calc_is_visa, method=True, type="boolean", string="Visa Payable", readonly=True)
                }
sale_order_line()