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

class crm_claim2meeting(osv.osv_memory):
    """ Converts Claim to Meeting"""

    _name = 'crm.claim2meeting'
    _description = 'Claim to meeting'
    
    
    def action_cancel(self, cr, uid, ids, context=None):
        """
        Closes Claim to Meeting form
        @param self: The object pointer
        @param cr: the current row, from the database cursor,
        @param uid: the current user’s ID for security checks,
        @param ids: List of Claim to Meeting IDs
        @param context: A standard dictionary for contextual values
        """

        return {'type':'ir.actions.act_window_close'}

    def view_init(self, cr, uid, fields, context=None):
        """
        This function checks for precondition before wizard executes
        @param self: The object pointer
        @param cr: the current row, from the database cursor,
        @param uid: the current user’s ID for security checks,
        @param fields: List of fields for default value
        @param context: A standard dictionary for contextual values

        """
        claim_obj = self.pool.get('crm.claim')
        record_id = context and context.get('active_id', False) or False
        claim = claim_obj.browse(cr, uid, record_id, context=context)
        meeting_obj = self.pool.get('crm.meeting').search(cr, uid, [])
        for meeting in meeting_obj:
            o_meeting = self.pool.get('crm.meeting').browse(cr,uid,meeting)
            if (o_meeting.crm_claim_id.id == claim.id):
                raise osv.except_osv(_("Warning"), _("Already created a meeting for this claim.\n Meeting ref: %s")%(o_meeting.name))


    def action_apply(self, cr, uid, ids, context=None):
        """
        This converts Claim to Meeting and opens Meeting view
        @param self: The object pointer
        @param cr: the current row, from the database cursor,
        @param uid: the current user’s ID for security checks,
        @param ids: List of Claim to Meeting IDs
        @param context: A standard dictionary for contextual values
        """
        record_id = context and context.get('active_id', False) or False
        if record_id:
            meet_obj = self.pool.get('crm.meeting')
            claim_obj = self.pool.get('crm.claim')
            case = claim_obj.browse(cr, uid, record_id, context=context)
            data_obj = self.pool.get('ir.model.data')
#            result = data_obj._get_id(cr, uid, 'crm', 'view_crm_case_opportunities_filter')
#            res = data_obj.read(cr, uid, result, ['res_id'])
            id2 = data_obj._get_id(cr, uid, 'crm', 'crm_case_form_view_meet')
            id3 = data_obj._get_id(cr, uid, 'crm', 'crm_case_tree_view_meet')
            id4 = data_obj._get_id(cr, uid, 'crm', 'crm_case_calendar_view_meet')
            id5 = data_obj._get_id(cr, uid, 'crm', 'crm_case_gantt_view_meet')
            if id2:
                id2 = data_obj.browse(cr, uid, id2, context=context).res_id
            if id3:
                id3 = data_obj.browse(cr, uid, id3, context=context).res_id
            if id4:
                id4 = data_obj.browse(cr, uid, id4, context=context).res_id
            if id5:
                id5 = data_obj.browse(cr, uid, id5, context=context).res_id
            
            
            for this in self.browse(cr, uid, ids, context=context):
                address = None
                user = this.user_id.id                
                organizer=""
                if user:
                    user_obj=self.pool.get('res.users').browse(cr, uid, user)
                    organizer = user_obj.name
                    if user_obj.user_email:
                        organizer = organizer + '<' + user_obj.user_email + '>' 
                if case.partner_id:
                    address_id = self.pool.get('res.partner').address_get(cr, uid, [case.partner_id.id])
                    if address_id['default']:
                        address = self.pool.get('res.partner.address').browse(cr, uid, address_id['default'], context=context)
                new_meet_id = meet_obj.create(cr, uid, {
                                'state':'draft',
                                'name': _('Claim: ') + case.name,
                                'partner_id': case.partner_id and case.partner_id.id or False,
                                'partner_address_id': address and address.id or False, 
                                'section_id': this.section_id.id or False,
                                'user_id': this.user_id.id or False,
                                'description': case.description or False,
                                'crm_claim_id': case.id,
                                'partner_phone':case.partner_id.phone or False,
                                'email_from':case.partner_id.email or False,
                                'categ_id': this.meeting_type.id,
                                'date':this.date,
                                'location':address.city or False,
                                'date_deadline':this.deadline,
                                'organizer':organizer,
                            })
                vals = {
                            'categ_id' : this.claim_category.id,
                            }
                claim_obj.write(cr, uid, [case.id], vals)

        value = {
            'name': _('Meeting'),
            'view_type': 'form',
            'view_mode': 'form,tree,calendar',
            'res_model': 'crm.meeting',
            'res_id': int(new_meet_id),
            'view_id': False,
            'views': [(id2, 'form'), (id3, 'tree'), (id4, 'calendar'), (id5, 'graph')],
            'type': 'ir.actions.act_window',
#            'search_view_id': res['res_id']
        }
        return value

    _columns = {
        'date' : fields.datetime('Start date',required=True),
        'deadline': fields.datetime('End date', required=True),
        'claim_category': fields.many2one('crm.case.categ', 'Claim category', required=True),
        'meeting_type': fields.many2one('crm.case.categ', 'Meeting Type', required=True),
        'user_id':fields.many2one('res.users', 'Manager'),
        'section_id':fields.many2one('crm.case.section', 'Sales Team'), 
        
        
    }

    def default_get(self, cr, uid, fields, context=None):
        """
        This function gets default values
        @param self: The object pointer
        @param cr: the current row, from the database cursor,
        @param uid: the current user’s ID for security checks,
        @param fields: List of fields for default value
        @param context: A standard dictionary for contextual values

        @return : default values of fields.
        """
        record_id = context and context.get('active_id', False) or False
        res = super(crm_claim2meeting, self).default_get(cr, uid, fields, context=context)
        if record_id:
            claim = self.pool.get('crm.claim').browse(cr, uid, record_id, context=context)
            if 'date' in fields:
                res.update({'date': time.strftime('%Y-%m-%d %H:%M:%S')})
            if 'deadline' in fields:
                if claim.date_deadline:
                    deadline = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(claim.date_deadline, '%Y-%m-%d'))
                else:
                    deadline = time.strftime('%Y-%m-%d %H:%M:%S')
                res.update({'deadline':deadline })
            if 'claim_category' in fields:
                res.update({'claim_category': claim.categ_id.id or False})
            if 'user_id' in fields:
                user = self.pool.get('res.users').search(cr,uid,[])
                res.update({'user_id': user[0] or False})
            if 'section_id' in fields:
                section = self.pool.get('crm.case.section').search(cr,uid,[('name', 'like', 'Dpto Instalaciones')])
                res.update({'section_id': section[0] or False})
        return res

crm_claim2meeting()