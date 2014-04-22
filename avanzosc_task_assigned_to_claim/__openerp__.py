# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc - Avanced Open Source Consulting
#    Copyright (C) 2011 - 2014 Avanzosc <http://www.avanzosc.com>
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
    "name": "Avanzosc Task Assigned to Claim",
    "version": "1.0",
    "depends": ["crm_claim","project"],
    "author": "AvanzOSC",
    "category": "Custom Modules",
    "description": """
        Avanzosc Custom Modules.
        Módulo que desde tareas linka con un one2many a reclamaciones y al revés, que en una reclamación se pueda ver a qué tarea corresponde. 

        DESCRIPCION de la reclamación, estará en una solapa aparte de NOTAS, en las reclamaciones. 
        DESCRIPCION de la solapa info-extra en tareas, estará en una solapa aparte NOTAS extra. 

        Por último, en tareas, la descripción de la solapa info-extra y la descripción como tal serán editables SIEMPRE. Sin estar limitado a estados de la tarea.

    """,
    "init_xml": [],
    'update_xml': ['crm_claim_ext_view.xml',
                   'project_task_ext_view.xml',
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': 'certificate',
}