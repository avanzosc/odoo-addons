
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

class report_contract_template_line(osv.osv):

    _name = 'report.contract.template.line'
    _description = 'Report Contract Template'
   
    _columns = {# Campo para saber a que plantilla pertenece la linea
                'report_contract_template_id':fields.many2one('report.contract.template', 'Report Contract Template'),
                # Campo para saber a que maestro de lineas de plantilla pertenece la linea
                'report_contract_template_master_line_id':fields.many2one('report.contract.template.master.line', 'Template Master Line'),
                # Código
                'code':fields.char('Code', size=64, required=True, select=1),
                # Nombre              
                'name':fields.char('Name', size=64, required=True, select=1),
                # Descripcion            
                'description':fields.text('Description', select=1),
                # Condiciones Generales
                'general_conditions': fields.boolean('General Conditions'),
                # Condiciones Particulares
                'particular_conditions': fields.boolean('Particular Conditions'),

                }   
    
    #
    ### SI CAMBIA EL TIPO DE COSTE
    #
    def onchange_master_line(self, cr, uid, ids, master_line_id, context=None):
        res={}
        if master_line_id:
            master_line_obj = self.pool.get('report.contract.template.master.line')
            master_line = master_line_obj.browse(cr, uid, master_line_id)
            res={'name': master_line.name,
                 'description': master_line.description,
                 } 
        return {'value': res}       
    
report_contract_template_line()
