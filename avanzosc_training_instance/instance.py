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

class instance(osv.osv):
    _name = 'instance'
    _description = 'instance'
    
    _columns = {
            
            'instance_number':fields.char('Instance number', size=128),
            'entry_date':fields.date('Entry Date'),
            'document_date':fields.date('Document Date'),
            'instance_type':fields.selection([('entry','Entry'),('output','Output'),('alumn','Alumn')],'Instance Type'),
            'source':fields.char('source', size=64),
            'sender':fields.char('sender', size=64),
            'extract':fields.char('extract', size=64),
            'active':fields.boolean('Active'),
            'contact_id':fields.many2one('res.partner.contact','Contact'),
            'document_id': fields.many2one('document','Document Type'),
    }
    _defaults = {
                 'active':lambda *a: 1,
                 }
instance()

class document(osv.osv):
 
    _inherit = 'document'
    
    _columns = {
                
        'instance_ids': fields.one2many('instance','document_id','Instances'),
    }
document()
