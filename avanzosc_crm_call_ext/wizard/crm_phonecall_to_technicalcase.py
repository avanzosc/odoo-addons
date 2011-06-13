# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc, OpenERP Professional Services   
#    Copyright (C) 2010-2011 Avanzosc S.L (http://www.avanzosc.com). All Rights Reserved
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

from osv import osv, fields
from tools.translate import _

class crm_phonecall2technicalcase(osv.osv_memory):
    """ Converts Phonecall to Technical case"""

    _name = 'crm.phonecall2technicalcase'
    _description = 'Phonecall To Technical case'

    def action_cancel(self, cr, uid, ids, context=None):
        """
        Closes Phonecall to Opportunity form
        @param self: The object pointer
        @param cr: the current row, from the database cursor,
        @param uid: the current user’s ID for security checks,
        @param ids: List of Phonecall to Technical case IDs
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
        phonecall_obj = self.pool.get('crm.phonecall')
        record_id = context and context.get('active_id', False) or False
        case = phonecall_obj.browse(cr, uid, record_id, context=context)
        if case.state in ['done', 'cancel']:
                raise osv.except_osv(_("Warning"), _("Closed/Cancelled Phone \
Call Could not convert into Technical Case"))
        if not case.description:
                raise osv.except_osv(_("Warning"), _("Phone \
Call without Description Could not convert into Technical Case"))
        if not case.section_id:
                raise osv.except_osv(_("Warning"), _("Phone \
Call without Sale Team Could not convert into Technical Case"))


    def action_apply(self, cr, uid, ids, context=None):
        """
        This converts Phonecall to Technical case and opens Phonecall view
        @param self: The object pointer
        @param cr: the current row, from the database cursor,
        @param uid: the current user’s ID for security checks,
        @param ids: List of Phonecall to Technical case IDs
        @param context: A standard dictionary for contextual values

        @return : Dictionary value for created Opportunity form
        """
        record_id = context and context.get('active_id', False) or False
        if record_id:
            tech_obj = self.pool.get('crm.helpdesk')
            phonecall_obj = self.pool.get('crm.phonecall')
            case = phonecall_obj.browse(cr, uid, record_id, context=context)
            data_obj = self.pool.get('ir.model.data')
#            result = data_obj._get_id(cr, uid, 'crm', 'view_crm_case_opportunities_filter')
#            res = data_obj.read(cr, uid, result, ['res_id'])
#            id2 = data_obj._get_id(cr, uid, 'crm', 'crm_case_form_view_oppor')
#            id3 = data_obj._get_id(cr, uid, 'crm', 'crm_case_tree_view_oppor')
#            if id2:
#                id2 = data_obj.browse(cr, uid, id2, context=context).res_id
#            if id3:
#                id3 = data_obj.browse(cr, uid, id3, context=context).res_id

            for this in self.browse(cr, uid, ids, context=context):
                address = None
                if this.partner_id:
                    address_id = self.pool.get('res.partner').address_get(cr, uid, [this.partner_id.id])
                    if address_id['default']:
                        address = self.pool.get('res.partner.address').browse(cr, uid, address_id['default'], context=context)
                new_technical_id = tech_obj.create(cr, uid, {
                                'name': this.name,
                                'partner_id': this.partner_id and this.partner_id.id or False,
                                'partner_address_id': address and address.id, 
                                'phone': address and address.phone,
                                'mobile': address and address.mobile,
                                'section_id': case.section_id and case.section_id.id,
                                'description': case.description or False,
                                'phonecall_id': case.id,
                                'canal_id': case.canal_id.id,
                                'priority': case.priority,
                                'user_id': case.section_id.user_id.id,
                                'phone': case.partner_phone or False,
                            })
                vals = {
                            'partner_id': this.partner_id.id,
                            'helpdesk_id' : new_technical_id,
                            }
                phonecall_obj.write(cr, uid, [case.id], vals)
                phonecall_obj.case_close(cr, uid, [case.id])
                tech_obj.case_open(cr, uid, [new_technical_id])

        value = {
            'name': _('Technical Case'),
            'view_type': 'form',
            'view_mode': 'form,tree',
            'res_model': 'crm.helpdesk',
            'res_id': int(new_technical_id),
            'view_id': False,
#            'views': [(id2, 'form'), (id3, 'tree'), (False, 'calendar'), (False, 'graph')],
            'type': 'ir.actions.act_window',
#            'search_view_id': res['res_id']
        }
        return value

    _columns = {
        'name' : fields.char('Case Summary', size=64, required=True, select=1),
        'partner_id': fields.many2one('res.partner', 'Partner', required=True),
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
        res = super(crm_phonecall2technicalcase, self).default_get(cr, uid, fields, context=context)

        if record_id:
            phonecall = self.pool.get('crm.phonecall').browse(cr, uid, record_id, context=context)
            if 'name' in fields:
                res.update({'name': phonecall.name})
            if 'partner_id' in fields:
                res.update({'partner_id': phonecall.partner_id and phonecall.partner_id.id or False})
        return res

crm_phonecall2technicalcase()