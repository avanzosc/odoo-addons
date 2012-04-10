# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2004-2010 Tiny SPRL (http://tiny.be). All Rights Reserved
#    Copyright (C) 2012 Avanzosc (http://Avanzosc.com). All Rights Reserved
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

class publication(osv.osv):
    _name = 'publication'
    _description = 'publication'
    
    _columns = {
            
            'contact_id': fields.many2one('res.partner.contact', 'Contact', required=True),
            'info':fields.char('Info', size=256),
            'production_type':fields.char('Production Type', size=128),
            'position':fields.char('Position Of Total', size=128),
            'as':fields.char('As', size=128),
            'impact_index':fields.char('Impact Index', size=128),
            'impact_agency':fields.char('Impact Agency', size=128),

    }
publication()
