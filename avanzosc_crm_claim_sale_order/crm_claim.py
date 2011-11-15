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

class crm_claim(osv.osv):
    _inherit = 'crm.claim'
    
    _columns={
             'sale_id':fields.many2one('sale.order', 'Sale Order'),
             'location':fields.char('Location', size=264, states={'done':[('readonly', True)]})
    }
 
    def onchange_section_id(self, cr, uid, ids, section_id): 
        values ={}
        section_obj = self.pool.get('crm.case.section')
        if section_id:
            section = section_obj.browse(cr,uid,section_id)
            values = {
                'user_id' : section.user_id.id,
            }
        return {'value' : values}
    def onchange_partner_id(self, cr, uid, ids, part, email=False):
        res = super(crm_claim, self).onchange_partner_id(cr, uid, ids, part, email)
        if part:
            partner = self.pool.get('res.partner').browse(cr, uid, part)
            if partner.address:
                add = partner.address[0].city
            else:
                add =''    
            res['value'].update({
                'location':add,
            })
        return res
crm_claim()