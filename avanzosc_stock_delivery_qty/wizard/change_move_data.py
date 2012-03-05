# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc - Avanced Open Source Consulting
#    Copyright (C) 2010 - 2011 Avanzosc <http://www.avanzosc.com>
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

import decimal_precision as dp

class change_stock_move(osv.osv):
    _name='change.stock.move'
    
    def view_init(self, cr, uid, fields, context=None):
        """
        This function checks for precondition before wizard executes
        @param self: The object pointer
        @param cr: the current row, from the database cursor,
        @param uid: the current user’s ID for security checks,
        @param fields: List of fields for default value
        @param context: A standard dictionary for contextual values

        """
        record_id = context.get('active_ids',[])
        if len(record_id)>1:
            raise osv.except_osv(_("Warning"), _("You can only modify a record at once"))
    _columns={
              'product_id':fields.many2one('product.product', 'Product', required=True),
              'qty':fields.float('Qty', digits_compute=dp.get_precision('Product UoM'), required=True),
              'price_unit':fields.float('Unit price', digits_compute= dp.get_precision('Account'), required=True),
              'lot_id':fields.many2one('stock.production.lot', 'Lot'),
              'location_id':fields.many2one('stock.location', 'Source', required=True),
              'location_dest_id':fields.many2one('stock.location', 'Destination', required=True),
              'date':fields.datetime('Date', required=True),
              }
    
    def action_apply(self, cr, uid, ids, context=None):
        """
        This converts Claim to Meeting and opens Meeting view
        @param self: The object pointer
        @param cr: the current row, from the database cursor,
        @param uid: the current user’s ID for security checks,
        @param ids: List of Claim to Meeting IDs
        @param context: A standard dictionary for contextual values
        """
        
        record_id = context and context.get('active_id', False) or False
        if record_id:
            change = self.browse(cr,uid,ids[0])
            self.pool.get('stock.move').write(cr,uid,[record_id], {'product_id': change.product_id.id, 'prodlot_id':change.lot_id.id, 'date':change.date, 'price_unit':change.price_unit, 'product_qty':change.qty, 'location_id':change.location_id.id, 'location_dest_id': change.location_dest_id.id})
        return {'type': 'ir.actions.act_window.close()'}
    
    def default_get(self, cr, uid, fields, context=None):
        """
        This function gets default values
        @param self: The object pointer
        @param cr: the current row, from the database cursor,
        @param uid: the current user’s ID for security checks,
        @param fields: List of fields for default value
        @param context: A standard dictionary for contextual values

        @return : default values of fields.
        """
        record_id = context and context.get('active_id', False) or False
        res = super(change_stock_move, self).default_get(cr, uid, fields, context=context)
        if record_id:
            move = self.pool.get('stock.move').browse(cr, uid, record_id, context=context)
            if 'date' in fields:
                res.update({'date': move.date or False})
            if 'product_id' in fields:
                res.update({'product_id':move.product_id.id or False})
            if 'lot_id' in fields:
                res.update({'lot_id': move.prodlot_id.id or False})
            if 'location_id' in fields:
                res.update({'location_id': move.location_id.id or False})
            if 'location_dest_id' in fields:
                res.update({'location_dest_id': move.location_dest_id.id or False})
            if 'qty' in fields:
                res.update({'qty': move.product_qty or False})
            if 'price_unit' in fields:
                res.update({'price_unit': move.price_unit or False})
        return res
    
change_stock_move()