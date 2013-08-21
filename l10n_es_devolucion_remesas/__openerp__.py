
# -*- encoding: utf-8 -*-
##############################################################################
#
#    7 i TRIA
#    Copyright (C) 2011 - 2012 7 i TRIA <http://www.7itria.cat>
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
{
    "name" : "Devoluciones de remesas.",
    "version" : "1.0",
    "depends" : ["account_payment_extension"],
    "author" : "7 i TRIA & Avanzosc, S.L.",
    "description": """
	Este módulo está basado en el módulo setitria_mods_comptabilitat. Actualizado y adaptado a la versión 6.0.3 por Avanzosc, S.L. 
    	Modulo que añade funcionalidad de introducción de asientos contables (recibos devueltos i gestión dinamica)
    """,
    'website': 'http://www.7itria.cat, http://www.avanzosc.com',
    'init_xml': [],     #los datos que necesitamos para que el modulo funcione
    'update_xml': [
            'security/setitria_mods_comptabilitat_security.xml',
            'security/ir.model.access.csv',
            'account_invoice_workflow.xml',
            'account_invoice_view.xml',
            'setitria_mods_comptabilitat.xml',
        ],   #las vistas, categorias de acceso, etc... (lo que se ha de cargar cada vez que se actualiza, etc...)
    'demo_xml': [],
    'installable': True,
    'active': False, #sirve para indicar si se quiere instalar cada vez que se crea una nueva BD (se instalaria automaticamente)
}
