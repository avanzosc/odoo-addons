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

from osv import osv, fields
from tools.translate import _
import time, datetime

class crm_lead2partner(osv.osv_memory):
    """ Converts lead to partner """

    _inherit = 'crm.lead2partner'
    _description = 'Lead to Partner'
    
    def _create_partner(self, cr, uid, ids, context=None):
        """
        This function Creates partner based on action.
        @param self: The object pointer
        @param cr: the current row, from the database cursor,
        @param uid: the current user’s ID for security checks,
        @param ids: List of Lead to Partner's IDs
        @param context: A standard dictionary for contextual values

        @return : Dictionary {}.
        """
        if context is None:
            context = {}
        #----------------------------------
        # OBJETOS
        #----------------------------------    
        lead_obj = self.pool.get('crm.lead')
        partner_obj = self.pool.get('res.partner')
        contact_obj = self.pool.get('res.partner.address')
        job_obj = self.pool.get('res.partner.job')
        contact2_obj = self.pool.get('res.partner.contact')
        partner_ids = []
        partner_id = False
        contact_id = False
        rec_ids = context and context.get('active_ids', [])
        
        for data in self.browse(cr, uid, ids, context=context):
            for lead in lead_obj.browse(cr, uid, rec_ids, context=context):
                if data.action == 'create':
                    #Creamos el res.partner.contact
                    valsConatact2={
                                   'name':lead.contact_surname,
                                   'first_name':lead.contact_name,
                    }
                    new_contact2_obj = contact2_obj.create(cr,uid,valsConatact2,context)
                    
                    partner_id = partner_obj.create(cr, uid, {
                        'name': lead.partner_name or lead.contact_name,
                        'user_id': lead.user_id.id,
                        'comment': lead.description,
                    })
                    contact_id = contact_obj.create(cr, uid, {
                        'partner_id': partner_id,
                        'name': lead.contact_resum,
                        'phone': lead.phone,
                        'mobile': lead.mobile,
                        'email': lead.email_from,
                        'fax': lead.fax,
                        'title': lead.title and lead.title.id or False,
                        'function': lead.function,
                        'street': lead.street,
                        'street2': lead.street2,
                        'zip': lead.zip,
                        'city': lead.city,
                        'country_id': lead.country_id and lead.country_id.id or False,
                        'state_id': lead.state_id and lead.state_id.id or False,
                    })
                    #creamos el res.patner.job
                    job = job_obj.create(cr,uid,{'contact_id':new_contact2_obj,'address_id':contact_id},context)

                else:
                    if data.partner_id:
                        partner_id = data.partner_id.id
                        contact_id = partner_obj.address_get(cr, uid, [partner_id])['default']

                partner_ids.append(partner_id)

                if data.action<>'no':
                    vals = {}
                    if partner_id:
                        vals.update({'partner_id': partner_id})
                    if contact_id:
                        vals.update({'partner_address_id': contact_id})
                    lead_obj.write(cr, uid, [lead.id], vals)
        return partner_ids
crm_lead2partner()