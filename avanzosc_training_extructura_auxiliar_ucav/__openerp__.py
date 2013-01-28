
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
{
    "name": "Avanzosc training extructura auxiliar ucav",
    "version": "1.0",
    "depends": ["base",
                "training",
                ],
    "author": "AvanzOSC",
    "category": "Custom Module",
    "website" : "www.avanzosc.com",
    "description": """
    This module provide 1 buttons to record:
        * Extra estructure for UCAV 
           
    The state of the new inscription will be 'draft' and as a responsible of the case, the corresponding responsible of the suscriptions team will be stablished as default.
    """,
    "init_xml": [],
    'update_xml': [
                   "training_antiguas_recibos_view.xml",
                   "training_antiguas_matriculas_view.xml",
                   "training_antiguas_actas_view.xml",
                   "training_antiguas_actas_proyectos_view.xml",
                   "training_antiguas_actacompensatorias_view.xml",
                   "menu_view.xml",
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
}