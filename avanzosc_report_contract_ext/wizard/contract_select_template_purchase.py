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
from datetime import datetime, timedelta
import time

from osv import osv
from osv import fields

from tools.translate import _
 
class contract_select_template_purchase(osv.osv_memory):

    _name = 'contract.select.template.purchase'
    _description = "Wizard Select Template"
 
    _columns = {
        'contract_template_id':fields.many2one('report.contract.template', 'Contract Template',domain=[('contract_type','=','P')]),
         }

    #
    ### Función
    #
    def template_selected_purchase(self, cr, uid, ids, context=None):
        #
        ### debo de cerrar el wizard de la siguiente manera
        #
        res={}
        
        contract_conditions_obj = self.pool.get('contract.conditions')
        
        simu_id = context.get('active_id')
        modelo = context.get('active_model')
        
        for wiz in self.browse(cr,uid,ids,context):
            if not wiz.contract_template_id:
                raise osv.except_osv('Insert Error', 'You must select one template')
                        
            src_temp = wiz.contract_template_id
            
            report_contract_template_obj = self.pool.get('report.contract.template')
            report_contract_template = report_contract_template_obj.browse(cr, uid,  wiz.contract_template_id.id)
            
            data={}

            for line1 in src_temp.general_conditions_lines_ids:
                #
                data = {'contract_type':report_contract_template.contract_type,
                        'code':line1.code,
                        'name':line1.name,
                        'description':line1.description,
                        'general_conditions':line1.general_conditions,
                        'particular_conditions':line1.particular_conditions,
                        'purchase_order1_ids': [(6, 0, [simu_id])],
                        }
            
                contract_conditions_obj.create(cr,uid,data)
            
            for line1 in src_temp.particular_conditions_lines_ids:
                #
                data = {'contract_type':report_contract_template.contract_type,
                        'code':line1.code,
                        'name':line1.name,
                        'description':line1.description,
                        'general_conditions':line1.general_conditions,
                        'particular_conditions':line1.particular_conditions,
                        'purchase_order2_ids': [(6, 0, [simu_id])],
                        }
            
                contract_conditions_obj.create(cr,uid,data)
                      
                
        return {'type': 'ir.actions.act_window_close'}
    
contract_select_template_purchase()