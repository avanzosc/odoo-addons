
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

class report_contract_template(osv.osv):

    _name = 'report.contract.template'
    _description = 'Report Contract Template'
   
    _columns = {# Nombre              
                'name':fields.char('Name', size=64, required=True, select=1),
                # Tipo
                'contract_type': fields.selection([('P', 'Purchase'),
                                                   ('S', 'Sale'),
                                                   ('R', 'RRHH')],
                                                  'Type', required=True, select=1),
                # Lineas de Condiciones Generales
                'general_conditions_lines_ids':fields.one2many('report.contract.template.line', 'report_contract_template_id', 'General Conditions', domain=[('general_conditions', '=', True)]),
                # Lineas de Condiciones particulares
                'particular_conditions_lines_ids':fields.one2many('report.contract.template.line', 'report_contract_template_id', 'Particular Conditions', domain=[('particular_conditions', '=', True)]),

                }   
    
report_contract_template()
