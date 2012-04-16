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

class artistic_work(osv.osv):
    _name = 'artistic.work'
    _description = 'artistic work'
    
    _columns = {
            
            'contact_id': fields.many2one('res.partner.contact', 'Contact'),
            'description':fields.char('Description', size=128),
            'denomination':fields.char('Exposure Denomination', size=128),
            'authors':fields.char('Authors', size=128),
            'city':fields.char('city', size=128),
            'type':fields.selection([('monographic','Monographic'),('catalog','Catalog'),('commissary','Commissary')],'Work Type'),
            'date':fields.date('Date'),
            'cataloging':fields.char('Cataloging', size=128),
            'prize':fields.char('Prize', size=128),
            'publication':fields.char('Publication', size=128),
            'other':fields.char('Other', size=128),
            
    }
artistic_work()
