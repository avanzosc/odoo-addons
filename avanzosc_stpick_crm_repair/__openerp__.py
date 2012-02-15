
# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2008 Daniel (Avanzosc) <danielcampos@avanzosc>
#    03/11/2011
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
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


{
    "name" : "Avanzosc Stock Picking CRM Repair",
    "version" : "1.0",
    "description": """ 
                This module adds:
                 - A link to crm claims in the stock pickings 
                 - A link to crm claims in repair orders
                 - For each crm claim, its associated Stock Pickings and repair orders list 
                 - For any product return it must have a crm claim linked.
                    """,
    "author": "AvanzOSC",
    "website" : "http://www.avanzosc.com",
    "depends" : ["base","crm_claim","mrp_repair"],
    "category" : "Generic Modules",
    "init_xml" : [],
    "demo_xml" : [],
    "update_xml" : ["stock_crm_picking_view.xml",
                    "crm_mrp_view.xml"],
    "active" : False,
    "installable" : True
    
}

