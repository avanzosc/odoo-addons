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
from tools.translate import _
import netsvc
class set_partner2lot(osv.osv_memory):
    
    _name="set.partner2lot"
    
    def button_ok(self, cr, uid, ids, context):
        
        production_obj = self.pool.get('mrp.production')
        lot_obj = self.pool.get('stock.production.lot')
        sale_obj = self.pool.get('sale.order')
        contact_obj = self.pool.get('res.partner.contact')
        
        sale_ids = context['active_ids']
    
        for sale in sale_obj.browse(cr, uid, sale_ids):
            customer = sale.partner_id.id
            address = sale.partner_shipping_id.id
            p_ids = production_obj.search(cr, uid, [('origin', '=', sale.name), ('state', '=', 'done')])
            for production_o in production_obj.browse(cr,uid,p_ids):
                installer = production_o.location_src_id.address_id.partner_id.id
                contact_list = contact_obj.search(cr,uid,[('partner_id', '=', installer)])
                technician = False
                if contact_list:
                    technician = contact_list[0]
                vals = {
                         'installer': installer,
                         'technician': technician,
                         'customer': customer,
                         'cust_address': address,
                        }
                for p_line in production_o.move_lines2:
                    p_lot = p_line.prodlot_id 
                    if p_lot:
                        if not p_lot.customer:                       
                            lot_obj.write(cr,uid,p_lot.id, vals)
                for p_line2 in production_o.move_created_ids2:
                    p_lot2 = p_line2.prodlot_id 
                    if p_lot2:
                        if not p_lot2.customer:
                            lot_obj.write(cr, uid, p_lot2.id, vals)
            
        return {'type': 'ir.actions.act_window_close'}                
set_partner2lot()
