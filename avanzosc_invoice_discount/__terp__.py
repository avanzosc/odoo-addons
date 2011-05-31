# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2007 Avanzosc (Daniel) www.avanzosc.com All Rights Reserved
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

{
    "name": "Avanzosc provider invoice discount",
    "version" : "1.0",
    "description" : """
        This module adds three new fields in the provider invoice form, allowing 
        to add 3 types of discounts to it 
        """,
    "author": "Avanzosc (Daniel and Urtzi Odriozola)",
    "website" : "www.avanzosc.com",
    "depends" : ["base","account"],
    "category" : "Generic Modules",
    "init_xml" : [],
    "demo_xml" : [],
    "update_xml" : ["avanzosc_invoice_discount_view.xml"],
    "active" : False,
    "installable" : True
    
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: