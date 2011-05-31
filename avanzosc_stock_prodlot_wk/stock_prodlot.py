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
import netsvc
import time
from tools.translate import _

class stock_production_lot(osv.osv):

    _inherit='stock.production.lot'
 
    _columns = {
            'state_history': fields.one2many('stock.prodlot.history', 'prodlot_id', 'History'),
            'customer': fields.many2one('res.partner', 'Customer', domain=[('customer', '=', True)], required=True),
            'state':fields.selection([
                ('active','Active'),
                ('inactive','Inactive'),
                ('cancel','Canceled'),
                ('nouse','No Used')], 'State', readonly=True),
    }
    
    _defaults = {  
        'state': lambda *a: 'active',
    }
    
    def action_active(self, cr, uid, ids):
        for id in ids:
            values = {
                 'date': time.strftime('%Y-%m-%d %H:%M:%S'),
                 'prodlot_id': id,
                 'rec_state': 'Active',     
            }
            self.pool.get('stock.prodlot.history').create(cr, uid, values)
            self.write(cr, uid, ids, {'state': 'active'})
        return True
        
    def action_inactive(self, cr, uid, ids): 
        for id in ids:
            print id
            values = {
                 'date': time.strftime('%Y-%m-%d %H:%M:%S'),
                 'prodlot_id': id,
                 'rec_state': 'Inactive',     
            }
            self.pool.get('stock.prodlot.history').create(cr, uid, values)
            self.write(cr, uid, ids, {'state': 'inactive'})
        return True
        
    def action_nouse(self, cr, uid, ids): 
        for id in ids:
            values = {
                 'date': time.strftime('%Y-%m-%d %H:%M:%S'),
                 'prodlot_id': id,
                 'rec_state': 'No Used',     
            }
            self.pool.get('stock.prodlot.history').create(cr, uid, values)
            self.write(cr, uid, ids, {'state': 'nouse'})
        return True
        
    def action_cancel(self, cr, uid, ids): 
        for id in ids:
            values = {
                 'date': time.strftime('%Y-%m-%d %H:%M:%S'),
                 'prodlot_id': id,
                 'rec_state': 'Canceled',     
            }
            self.pool.get('stock.prodlot.history').create(cr, uid, values)
            self.write(cr, uid, ids, {'state': 'cancel'})
        return True
stock_production_lot()

class stock_prodlot_history(osv.osv):

    _name = 'stock.prodlot.history'
    _description = 'Product Lot Movement History'
 
    _columns = {
            'description':fields.char('Description', size=64),
            'prodlot_id': fields.many2one('stock.production.lot', required=True),
            'date': fields.date('Date', required=True, readonly=True),
            'rec_state': fields.char('state', size=64, required=True, readonly=True),
    }
stock_prodlot_history()