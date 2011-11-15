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

import time
from osv import osv
from osv import fields

class crm_claim_create_wizard(osv.osv_memory):
    _name = 'crm.claim.create.wizard'
    _description = 'Wizard to create a claim from sale order'
 
    _columns = {
        'name':fields.char('Claim Subject', size=64, required=True),
        'claim_date':fields.datetime('Claim Date'),
        'section_id':fields.many2one('crm.case.section', 'Sales Team'),
    }
    
    _defaults = {  
        'claim_date': lambda *a: time.strftime('%Y/%m/%d %H:%M:%S'),
    }
    
    def create_claim(self, cr, uid, ids, context=None):
        values={}
        claim_obj = self.pool.get('crm.claim')
        saleorder_obj = self.pool.get('sale.order')
        for wizard in self.browse(cr, uid, ids):
            sale = saleorder_obj.browse(cr, uid, context['active_id'])
            values = {
                'name': wizard.name,
                'partner_id':sale.partner_id.id,
                'sale_id': sale.id,
            }
            for address in sale.partner_id.address:
                values.update({
                    'partner_address_id': address.id,
                    'partner_phone': address.phone,
                    'email_from': address.email,
                })
            if wizard.claim_date:
                values.update({
                    'claim_date': wizard.claim_date,
                })
            if wizard.section_id:
                values.update({
                    'section_id': wizard.section_id.id, 
                })
                if wizard.section_id.user_id:
                    values.update({
                        'user_id': wizard.section_id.user_id.id, 
                    })  
            claim_obj.create(cr, uid, values)
        return {'type': 'ir.actions.act_window_close'}
    
    
crm_claim_create_wizard()
