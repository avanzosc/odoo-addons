
# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2004-2010 Tiny SPRL (http://tiny.be). All Rights Reserved
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

class sale_order(osv.osv):

    _name = 'sale.order'
    _inherit = 'sale.order'
   
    _columns = {# Campo para saber que condiciones estas relacionadas con el pedido de compra (CONDICIONES GENERALES)
                'general_contract_conditions_ids': fields.many2many('contract.conditions','gcontractconditions_saleorder_rel','sale_order_id','contract_conditions_id', 'General Contract Conditions', domain=[('contract_type','=','S'),('general_conditions','=',True)]),
                # Campo para saber que condiciones estas relacionadas con el pedido de compra (CONDICIONES PARTICULARES)
                'particular_contract_conditions_ids': fields.many2many('contract.conditions','pcontractconditions_saleorder_rel','sale_order_id','contract_conditions_id', 'Particular Contract Conditions', domain=[('contract_type','=','S'),('particular_conditions','=',True)]),
                }
    
sale_order()
