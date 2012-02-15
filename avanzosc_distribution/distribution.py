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

from osv import osv
from osv import fields

class res_users(osv.osv):
    _inherit = 'res.users'
 
    _columns = {
        'partner_id':fields.many2one('res.partner','Partner'),
    }
res_users()

class sale_order(osv.osv):
    _inherit = 'sale.order'
 
    _columns = {
        'installer_partner':fields.many2one('res.partner','Installer Partner'),
        'commercial_partner':fields.many2one('res.partner','Commercial Partner'),
    }
sale_order()

class crm_meeting(osv.osv):
    _inherit = 'crm.meeting'
 
    _columns = {
        'installer_partner':fields.many2one('res.partner','Installer Partner'),
        'commercial_partner':fields.many2one('res.partner','Commercial Partner'),
    }
crm_meeting()

class crm_helpdesk(osv.osv):
    _inherit = 'crm.helpdesk'
 
    _columns = {
        'installer_partner':fields.many2one('res.partner','Installer Partner'),
        'commercial_partner':fields.many2one('res.partner','Commercial Partner'),
    }
crm_helpdesk()

class res_partner(osv.osv):
    _inherit = 'res.partner'
 
    _columns = {
        'installer_partner':fields.many2one('res.partner','Installer Partner'),
        'commercial_partner':fields.many2one('res.partner','Commercial Partner'),
    }
res_partner()