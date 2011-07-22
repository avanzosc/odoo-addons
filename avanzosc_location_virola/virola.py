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


from osv import osv, fields
from tools.translate import _

class stock_location(osv.osv):    
    _inherit = 'stock.location'
    
    _columns = {
                'virola': fields.integer('Num. Virola', size = 5),
                'capvirola':fields.float('Cap. por virola', digits = (10,2)),
                
                }   
stock_location()

class stock_inventory_line(osv.osv):
    _inherit = "stock.inventory.line"
    
    _columns = {
                'virola': fields.float('Virola', digits = (10,2)),
                }
    
    def onchange_virola(self, cr, uid, fields, virola, location_id, context=None):
        res = {}
        if location_id:            
            location = self.pool.get('stock.location').browse(cr,uid,location_id)
            num_vir = location.virola
            if (num_vir >=  virola):
                
                cap_vir = location.capvirola
                qty = virola * cap_vir
                res = {
                       'product_qty':qty,
                }
            else: 
                raise osv.except_osv(_('Error!'),_('You have exceeded the limit of number of sleeves.'))
        return {'value': res} 
    
stock_inventory_line()

