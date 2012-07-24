# -*- encoding: utf-8 -*-
##############################################################################
#
#    AvanzOSC, Avanzed Open Source Consulting 
#    Copyright (C) 2011-2012 Iker Coranti (www.avanzosc.com). All Rights Reserved
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

class res_partner_contact(osv.osv):

    _inherit = 'res.partner.contact'
 
    _columns = {
            'type': fields.selection([('student','Student'),('teacher','Teacher'),('other','Other')],'Type'),
            'state_id':fields.many2one('res.country.state','State'),
            'profession':fields.char('Profession', size=64),
            'parent_studies':fields.char('Parent studies', size=64),
            'access_year': fields.integer('Access year'),
            'authorized_person_ids':fields.one2many('authorized.person', 'contact_id', "Authorized People"),
            'tutor':fields.many2one('res.partner.contact','Tutor'),
        }
    _defaults = {
                 'type':lambda *a: 'student',
                 }
res_partner_contact()
