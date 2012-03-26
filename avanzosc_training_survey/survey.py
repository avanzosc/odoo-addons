# -*- encoding: utf-8 -*-
##############################################################################
#
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

from osv import osv,fields

class survey_name_wiz(osv.osv_memory):
    _inherit = 'survey.name.wiz'
    _name = 'survey.name.wiz'
    _columns={
              'partner_id':fields.many2one('res.partner', 'Customer'),
              'address_id':fields.many2one('res.address', 'Address'),
              'user_id':fields.many2one('res.user', 'User'),            
              }
survey_name_wiz()








