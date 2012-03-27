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
              'address_id':fields.many2one('res.partner.address', 'Address'),         
              }
survey_name_wiz()


class survey_answer_list(osv.osv):    
    _name='survey.answer.list'    
    _columns={
              'name': fields.char('Name', size=128),
              'date':fields.date('Date'),
              'partner_id': fields.many2one('res.partner', 'Customer'),
              'address_id': fields.many2one('res.partner.address', 'Address'),
              'user_id': fields.many2one('res.users', 'User'),
              'answer_ids': fields.one2many('survey.response.answer', 'list_id', 'Answers'), 
              }
survey_answer_list()

class survey_response_answer(osv.osv):
    _inherit='survey.response.answer'
    _columns={
              'list_id': fields.many2one('survey.answer.list', 'List'),
              }

survey_response_answer()


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