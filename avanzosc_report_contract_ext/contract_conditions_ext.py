
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

class contract_conditions(osv.osv):

    _name = 'contract.conditions'
    _inherit = 'contract.conditions'
    
    _order= 'code'
   
    _columns = {# Tipo
                'contract_type': fields.selection([('P', 'Purchase'),
                                                   ('S', 'Sale'),
                                                   ('R', 'RRHH')],
                                                  'Type', required=True, select=1),
                # Código
                'code':fields.char('Code', size=64, required=True, select=1),
                # Descripcion            
                'description':fields.text('Description', select=1),
                # Condiciones Generales
                'general_conditions': fields.boolean('General Conditions'),
                # Condiciones Particulares
                'particular_conditions': fields.boolean('Particular Conditions'),
                # Campo para saber a que pedidos de compra esta asociado las condiciones de contrato (CONDICIONES GENERALES)
                'purchase_order1_ids': fields.many2many('purchase.order','gcontractconditions_purchaseorder_rel','contract_conditions_id','purchase_order_id','Purchase Orders'),
                # Campo para saber a que pedidos de compra esta asociado las condiciones de contrato (CONDICIONES PARTICULARES)
                'purchase_order2_ids': fields.many2many('purchase.order','pcontractconditions_purchaseorder_rel','contract_conditions_id','purchase_order_id','Purchase Orders'),
                # Campo para saber a que pedidos de compra esta asociado las condiciones de contrato (CONDICIONES GENERALES)
                'sale_order1_ids': fields.many2many('sale.order','gcontractconditions_saleorder_rel','contract_conditions_id','sale_order_id','Sale Orders'),
                # Campo para saber a que pedidos de compra esta asociado las condiciones de contrato (CONDICIONES PARTICULARES)
                'sale_order2_ids': fields.many2many('sale.order','pcontractconditions_saleorder_rel','contract_conditions_id','sale_order_id','Sale Orders'),
                # Campo para saber a que pedidos de compra esta asociado las condiciones de contrato (CONDICIONES GENERALES)
                'hrcontract_order1_ids': fields.many2many('hr.contract','gcontractconditions_hrcontract_rel','contract_conditions_id','hr_contract_id','Contracts'),
                # Campo para saber a que pedidos de compra esta asociado las condiciones de contrato (CONDICIONES PARTICULARES)
                'hrcontract_order2_ids': fields.many2many('hr.contract','pcontractconditions_hrcontract_rel','contract_conditions_id','hr_contract_id','Contracts'),
                }   
    
contract_conditions()
