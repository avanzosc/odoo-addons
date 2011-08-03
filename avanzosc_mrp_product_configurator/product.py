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
            'selection_type': fields.selection([
                ('one','One'),
                ('multiple','Multiple')], 'Select'),
            'alt_product_ids':fields.many2many('product.product', 'alt_product_rel', 'generic_prod', 'alt_prod', 'Product List', domain=[('sale_ok', '=', True)]),
    }
    
    _defaults = {  
        'selection_type': lambda *a: 'one',
    }
product_product()