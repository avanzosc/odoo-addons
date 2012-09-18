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

class product_product(osv.osv):
    _inherit = 'product.product'
    
    _columns = {
        'training_charges': fields.selection([
            ('fee','Fee'),
            ('recog','Recognition'),
            ('course','Course'),
            ('subject','Subject'),
            ('other','Other'),
            ], 'Training Charge'),
    
        'descount':fields.integer('Descount %'),
        'price_rates':fields.float('Price in Rates'),
        'applying_unit':fields.many2one('product.uom', 'Applying Unit', required=True),
    }
    
#    _defaults = {
#        
#        'applying_unit': _get_uom_id,
#        
#    }
#    
#    def _get_uom_id(self, cr, uid, *args):
#        cr.execute('select id from product_uom order by id limit 1')
#        res = cr.fetchone()
#        return res and res[0] or False
    
product_product()

#class training_fee_master(osv.osv):
#    _name = 'training.fee.master'
#    _description = 'Fee Master Table'
# 
#    _columns = {
#            'name': fields.char('Description', size=64),
#            'value': fields.float('Value'),
#        }
#training_fee_master()
#
#class training_recog_master(osv.osv):
#    _name = 'training.recog.master'
#    _description = 'Recognition Master Table'
# 
#    _columns = {
#            'name': fields.char('Description', size=64),
#            'value': fields.float('Value'),
#    }
#training_recog_master()