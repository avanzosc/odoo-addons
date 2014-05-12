
# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2008-2013 AvanzOSC (Daniel). All Rights Reserved
#    Date: 13/11/2013
#    
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
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



{
    'name': 'Avanzosc Copy Sale Order',
    'version': "1.01",
    'category': "Generic Modules",
    'author': 'AvanzOSC',
    'website': 'www.avanzosc.com',
    'depends': ['sale'],
    'init_xml': [],
    'update_xml': [],
    'demo_xml': [],
    'installable': True,
    'active': False,
    'description': """
     Con este módulo cuando se duplica un pedido de venta, no genera secuencia.
     Generará secuencia cuando se grabe el pedido de venta.
 		""",
}

