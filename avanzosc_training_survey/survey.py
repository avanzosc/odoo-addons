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
import time
class survey_name_wiz(osv.osv_memory):
    _inherit = 'survey.name.wiz'
    _name = 'survey.name.wiz'
    _columns={
              'partner_id':fields.many2one('res.partner', 'Customer'),
              'address_id':fields.many2one('res.partner.address', 'Address'),         
              }
    
    def onchange_partner(self, cr, uid, ids, partner_id, context=None):
        res = {}
        if partner_id:            
            address = self.pool.get('res.partner.address').search(cr,uid,[('partner_id','=',partner_id)])            
            if address:
                res = {
                    'address_id': address[0],
                    }
        return {'value': res} 
    def action_next(self, cr, uid, ids, context=None):
        """
        Start the survey, Increment in started survey field but if set the max_response_limit of
        survey then check the current user how many times start this survey. if current user max_response_limit
        is reach then this user can not start this survey(Raise Exception).

        @param self: The object pointer
        @param cr: the current row, from the database cursor,
        @param uid: the current user’s ID for security checks,
        @param ids: List of Survey IDs
        @param context: A standard dictionary for contextual values
        @return : Dictionary value for open survey question wizard.
        """
        survey_obj = self.pool.get('survey')
        search_obj = self.pool.get('ir.ui.view')
        if context is None: context = {}

        sur_id = self.read(cr, uid, ids, [])[0]
        survey_id = sur_id['survey_id']
        context.update({'survey_id': survey_id, 'sur_name_id': sur_id['id']})
        cr.execute('select count(id) from survey_history where user_id=%s\
                    and survey_id=%s' % (uid,survey_id))

        res = cr.fetchone()[0]
        user_limit = survey_obj.read(cr, uid, survey_id, ['response_user'])['response_user']
        if user_limit and res >= user_limit:
            raise osv.except_osv(_('Warning !'),_("You can not give response for this survey more than %s times") % (user_limit))

        sur_rec = survey_obj.read(cr,uid,self.read(cr,uid,ids)[0]['survey_id'])
        if sur_rec['max_response_limit'] and sur_rec['max_response_limit'] <= sur_rec['tot_start_survey']:
            raise osv.except_osv(_('Warning !'),_("You can not give more response. Please contact the author of this survey for further assistance."))

        search_id = search_obj.search(cr,uid,[('model','=','survey.question.wiz'),('name','=','Survey Search')])
        ###################################################
        #              AvanzOSC CODE(START)               #
        ###################################################
        address = False
        partner = False
        
        if sur_id['address_id']:
            address = sur_id['address_id']
        if sur_id['partner_id']:
            partner = sur_id['address_id']
            
        context.update({'address_id': address, 'partner_id':partner})
        ###################################################
        #                AvanzOSC CODE(END)               #
        ###################################################
        return {
            'view_type': 'form',
            "view_mode": 'form',
            'res_model': 'survey.question.wiz',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'search_view_id': search_id[0],
            'context': context
        }
survey_name_wiz()


class survey_response(osv.osv):
    _inherit='survey.response'
    _columns={
              'partner_id': fields.many2one('res.partner', 'Partner'),
              'address_id': fields.many2one('res.partner.address', 'Address'),
              }
survey_response()


class survey_response_line(osv.osv):
    _inherit='survey.response.line'
    _rec_name='name'
     
    def _get_name(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for record in self.browse(cr, uid, ids, context):
            name= record.question_id.question
            res[record.id] = name 
        return res
    _columns={
              'name':fields.function(_get_name, method=True, type='char', size=500, store=False),
              
              }

survey_response_line()