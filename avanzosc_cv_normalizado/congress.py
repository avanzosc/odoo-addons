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

class congress(osv.osv):
    _name = 'congress'
    _description = 'congress'
    
    _columns = {
            
            'contact_id': fields.many2one('res.partner.contact', 'Contact', required=True),
            'denomination':fields.char('Event Denomination', size=128),
            'participation_type':fields.char('Participation Type', size=128, required=True),
            'thesis_codirector':fields.char('Thesis Codirector', size=128),
            'objectives':fields.char('Objectives', size=128),
            'receiver_profile':fields.char('Receiver Profile', size=128),
            'city':fields.char('City', size=128),
            'presentation_date':fields.date('Presentation Date'),
            'entity':fields.char('City', size=128),
            'issn':fields.integer('ISSN'),      
    }
congress()
