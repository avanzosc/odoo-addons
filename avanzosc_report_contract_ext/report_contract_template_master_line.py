
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

class report_contract_template_master_line(osv.osv):

    _name = 'report.contract.template.master.line'
    _description = 'Report Contract Template Master Line'
   
    _columns = {# Nombre              
                'name':fields.char('Name', size=64, required=True, select=1),
                # Descripcion            
                'description':fields.text('Description', select=1),
                # Campo para saber con que lineas de plantillas de contrato esta relacionada
                'contract_template_lines_ids':fields.one2many('report.contract.template.line', 'report_contract_template_master_line_id', 'Contract Template Lines'),
                }   
    
report_contract_template_master_line()
