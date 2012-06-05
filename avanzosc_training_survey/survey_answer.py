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


import os
import datetime
from lxml import etree
from time import strftime
import time
import tools
import netsvc
from osv import osv
from osv import fields
from tools import to_xml
from tools.translate import _
import addons

class survey_question_wiz(osv.osv_memory):
    _inherit = 'survey.question.wiz'

    def create(self, cr, uid, vals, context=None):
        """
        Create the Answer of survey and store in survey.response object, and if set validation of question then check the value of question if value is wrong then raise the exception.

        @param self: The object pointer
        @param cr: the current row, from the database cursor,
        @param uid: the current user’s ID for security checks,
        @param vals: Values,
        @param context: A standard dictionary for contextual values
        @return : True.
        """
        if context is None: context = {}
        if context.has_key('active') and context.get('active',False):
            return True
    
        for key,val in vals.items():
            if key.split('_')[0] == "progress":
                vals.pop(key)
            if not context.has_key('sur_name_id') and key.split('_')[0] == "wizardid":
                context.update({'sur_name_id': int(key.split('_')[1])})
                vals.pop(key)

        click_state = True
        click_update = []
        surv_name_wiz = self.pool.get('survey.name.wiz')
        surv_all_resp_obj = self.pool.get('survey.response')
        surv_tbl_column_obj = self.pool.get('survey.tbl.column.heading')
        survey_obj = self.pool.get('survey')
        resp_obj = self.pool.get('survey.response.line')
        res_ans_obj = self.pool.get('survey.response.answer')
        que_obj = self.pool.get('survey.question')
        sur_name_read = surv_name_wiz.read(cr, uid, context.get('sur_name_id',False), [])
        response_id =  0
        
        if not sur_name_read['response']:
            response_id = surv_all_resp_obj.create(cr, uid, {'response_type':'link', 'user_id':uid, 'date_create':datetime.datetime.now(), 'survey_id' : context['survey_id']})
            surv_name_wiz.write(cr, uid, [context.get('sur_name_id', False)], {'response' : tools.ustr(response_id)})
        else:
            response_id = int(sur_name_read['response'])
        ###########################################
        #          AvanzOSC CODE(START)           #
        ###########################################
        partner = False
        address = False
        ref = False
        project = False
        product = False
        sale = False
        task = False
        production = False
        picking = False
        
        if 'partner_id' in context:
            partner = context['partner_id']
        if 'address_id' in context:
            address = context['address_id']
        if 'ref' in context:
            ref = context['ref']
        if 'project_id' in context:
            project = context['project_id']
        if 'product_id' in context:
            product = context['product_id']
        if 'sale_id' in context:
            sale = context['sale_id']
        if 'task_id' in context:
            task = context['task_id']
        if 'production_id' in context:
            production = context['production_id']
        if 'picking_id' in context:
            picking = context['picking_id']
        surv_all_resp_obj.write(cr,uid,[response_id], {'partner_id':partner, 'address_id':address, 'ref':ref, 'sale_id':sale, 'project_id':project, 'product_id':product, 'picking_id':picking, 'task_id':task, 'production_id':production})
        ###########################################
        #           AvanzOSC CODE(END)            #
        ###########################################
        
        if response_id not in surv_all_resp_obj.search(cr, uid, []):
            response_id = surv_all_resp_obj.create(cr, uid, {'response_type':'link', 'user_id':uid, 'date_create':datetime.datetime.now(), 'survey_id' : context.get('survey_id',False)})
            surv_name_wiz.write(cr, uid, [context.get('sur_name_id',False)], {'response' : tools.ustr(response_id)})


        
        #click first time on next button then increemnet on total start suvey
        if not sur_name_read['store_ans']:
            his_id = self.pool.get('survey.history').create(cr, uid, {'user_id': uid, \
                                              'date': strftime('%Y-%m-%d %H:%M:%S'), 'survey_id': sur_name_read['survey_id']})
            sur_rec = survey_obj.read(cr, uid, sur_name_read['survey_id'])
            survey_obj.write(cr, uid, sur_name_read['survey_id'],  {'tot_start_survey' : sur_rec['tot_start_survey'] + 1})
            if context.has_key('cur_id'):
                if context.has_key('request') and context.get('request',False):
                    self.pool.get(context.get('object',False)).write(cr, uid, [int(context.get('cur_id',False))], {'response' : response_id})
                    self.pool.get(context.get('object',False)).survey_req_done(cr, uid, [int(context.get('cur_id'))], context)
                else:
                    self.pool.get(context.get('object',False)).write(cr, uid, [int(context.get('cur_id',False))], {'response' : response_id})
        if sur_name_read['store_ans'] and type(sur_name_read['store_ans']) == dict:
            for key,val in sur_name_read['store_ans'].items():
                for field in vals:
                    if field.split('_')[0] == val['question_id']:
                        click_state = False
                        click_update.append(key)
                        break
        else:
            sur_name_read['store_ans'] = {}
        if click_state:
            que_li = []
            resp_id_list = []
            for key, val in vals.items():
                que_id = key.split('_')[0]
                if que_id not in que_li:
                    que_li.append(que_id)
                    que_rec = que_obj.read(cr, uid, [int(que_id)], [])[0]
                    res_data =  {
                        'question_id': que_id,
                        'date_create': datetime.datetime.now(),
                        'state': 'done',
                        'response_id': response_id
                    }
                    resp_id = resp_obj.create(cr, uid, res_data)
                    resp_id_list.append(resp_id)
                    sur_name_read['store_ans'].update({resp_id:{'question_id':que_id}})
                    surv_name_wiz.write(cr, uid, [context.get('sur_name_id',False)], {'store_ans':sur_name_read['store_ans']})
                    select_count = 0
                    numeric_sum = 0
                    selected_value = []
                    matrix_list = []
                    comment_field = False
                    comment_value = False
                    response_list = []

                    for key1, val1 in vals.items():
                        if val1 and key1.split('_')[1] == "table" and key1.split('_')[0] == que_id:
                            surv_tbl_column_obj.create(cr, uid, {'response_table_id' : resp_id,'column_id':key1.split('_')[2], 'name':key1.split('_')[3], 'value' : val1})
                            sur_name_read['store_ans'][resp_id].update({key1:val1})
                            select_count += 1

                        elif val1 and key1.split('_')[1] == "otherfield" and key1.split('_')[0] == que_id:
                            comment_field = True
                            sur_name_read['store_ans'][resp_id].update({key1:val1})
                            select_count += 1
                            surv_name_wiz.write(cr, uid, [context.get('sur_name_id',False)], {'store_ans':sur_name_read['store_ans']})
                            continue

                        elif val1 and key1.split('_')[1] == "selection" and key1.split('_')[0] == que_id:
                            if len(key1.split('_')) > 2:
                                ans_create_id = res_ans_obj.create(cr, uid, {'response_id':resp_id, 'answer_id':key1.split('_')[-1], 'column_id' : val1})
                                selected_value.append(val1)
                                response_list.append(str(ans_create_id) + "_" + str(key1.split('_')[-1]))
                            else:
                                ans_create_id = res_ans_obj.create(cr, uid, {'response_id':resp_id, 'answer_id':val1})
                            sur_name_read['store_ans'][resp_id].update({key1:val1})
                            select_count += 1

                        elif key1.split('_')[1] == "other" and key1.split('_')[0] == que_id:
                            if not val1:
                                comment_value = True
                            else:
                                error = False
                                if que_rec['is_comment_require'] and que_rec['comment_valid_type'] == 'must_be_specific_length':
                                    if (not val1 and  que_rec['comment_minimum_no']) or len(val1) <  que_rec['comment_minimum_no'] or len(val1) > que_rec['comment_maximum_no']:
                                        error = True
                                elif que_rec['is_comment_require'] and  que_rec['comment_valid_type'] in ['must_be_whole_number', 'must_be_decimal_number', 'must_be_date']:
                                    error = False
                                    try:
                                        if que_rec['comment_valid_type'] == 'must_be_whole_number':
                                            value = int(val1)
                                            if value <  que_rec['comment_minimum_no'] or value > que_rec['comment_maximum_no']:
                                                error = True
                                        elif que_rec['comment_valid_type'] == 'must_be_decimal_number':
                                            value = float(val1)
                                            if value <  que_rec['comment_minimum_float'] or value > que_rec['comment_maximum_float']:
                                                error = True
                                        elif que_rec['comment_valid_type'] == 'must_be_date':
                                            value = datetime.datetime.strptime(val1, "%Y-%m-%d")
                                            if value <  datetime.datetime.strptime(que_rec['comment_minimum_date'], "%Y-%m-%d") or value >  datetime.datetime.strptime(que_rec['comment_maximum_date'], "%Y-%m-%d"):
                                                error = True
                                    except:
                                        error = True
                                elif que_rec['is_comment_require'] and  que_rec['comment_valid_type'] == 'must_be_email_address':
                                    import re
                                    if re.match("^[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$", val1) == None:
                                            error = True
                                if error:
                                    for res in resp_id_list:
                                        sur_name_read['store_ans'].pop(res)
                                    raise osv.except_osv(_('Warning !'), "'" + que_rec['question'] + "'  \n" + tools.ustr(que_rec['comment_valid_err_msg']))

                                resp_obj.write(cr, uid, resp_id, {'comment':val1})
                                sur_name_read['store_ans'][resp_id].update({key1:val1})

                        elif val1 and key1.split('_')[1] == "comment" and key1.split('_')[0] == que_id:
                            resp_obj.write(cr, uid, resp_id, {'comment':val1})
                            sur_name_read['store_ans'][resp_id].update({key1:val1})
                            select_count += 1

                        elif val1 and key1.split('_')[0] == que_id and (key1.split('_')[1] == "single"  or (len(key1.split('_')) > 2 and key1.split('_')[2] == 'multi')):
                            error = False
                            if que_rec['is_validation_require'] and que_rec['validation_type'] == 'must_be_specific_length':
                                if (not val1 and  que_rec['validation_minimum_no']) or len(val1) <  que_rec['validation_minimum_no'] or len(val1) > que_rec['validation_maximum_no']:
                                    error = True
                            elif que_rec['is_validation_require'] and que_rec['validation_type'] in ['must_be_whole_number', 'must_be_decimal_number', 'must_be_date']:
                                error = False
                                try:
                                    if que_rec['validation_type'] == 'must_be_whole_number':
                                        value = int(val1)
                                        if value <  que_rec['validation_minimum_no'] or value > que_rec['validation_maximum_no']:
                                            error = True
                                    elif que_rec['validation_type'] == 'must_be_decimal_number':
                                        value = float(val1)
                                        if value <  que_rec['validation_minimum_float'] or value > que_rec['validation_maximum_float']:
                                            error = True
                                    elif que_rec['validation_type'] == 'must_be_date':
                                        value = datetime.datetime.strptime(val1, "%Y-%m-%d")
                                        if value <  datetime.datetime.strptime(que_rec['validation_minimum_date'], "%Y-%m-%d") or value >  datetime.datetime.strptime(que_rec['validation_maximum_date'], "%Y-%m-%d"):
                                            error = True
                                except:
                                    error = True
                            elif que_rec['is_validation_require'] and que_rec['validation_type'] == 'must_be_email_address':
                                import re
                                if re.match("^[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$", val1) == None:
                                        error = True
                            if error:
                                for res in resp_id_list:
                                    sur_name_read['store_ans'].pop(res)
                                raise osv.except_osv(_('Warning !'), "'" + que_rec['question'] + "'  \n" + tools.ustr(que_rec['validation_valid_err_msg']))

                            if key1.split('_')[1] == "single" :
                                resp_obj.write(cr, uid, resp_id, {'single_text':val1})
                            else:
                                ans_create_id = res_ans_obj.create(cr, uid, {'response_id':resp_id, 'answer_id':key1.split('_')[1], 'answer' : val1})

                            sur_name_read['store_ans'][resp_id].update({key1:val1})
                            select_count += 1

                        elif val1 and que_id == key1.split('_')[0] and len(key1.split('_')) > 2 and key1.split('_')[2] == 'numeric':
                            if not val1=="0":
                                try:
                                    numeric_sum += int(val1)
                                    ans_create_id = res_ans_obj.create(cr, uid, {'response_id':resp_id, 'answer_id':key1.split('_')[1], 'answer' : val1})
                                    sur_name_read['store_ans'][resp_id].update({key1:val1})
                                    select_count += 1
                                except:
                                    for res in resp_id_list:
                                        sur_name_read['store_ans'].pop(res)
                                    raise osv.except_osv(_('Warning !'), "'" + que_rec['question'] + "' \n" + _("Please enter an integer value"))

                        elif val1 and que_id == key1.split('_')[0] and len(key1.split('_')) == 3:
                            if type(val1) == type('') or type(val1) == type(u''):
                                ans_create_id = res_ans_obj.create(cr, uid, {'response_id':resp_id, 'answer_id':key1.split('_')[1], 'column_id' : key1.split('_')[2], 'value_choice' : val1})
                                sur_name_read['store_ans'][resp_id].update({key1:val1})
                            else:
                                ans_create_id = res_ans_obj.create(cr, uid, {'response_id':resp_id, 'answer_id':key1.split('_')[1], 'column_id' : key1.split('_')[2]})
                                sur_name_read['store_ans'][resp_id].update({key1:True})

                            matrix_list.append(key1.split('_')[0] + '_' + key1.split('_')[1])
                            select_count += 1

                        elif val1 and que_id == key1.split('_')[0] and len(key1.split('_')) == 2:
                            ans_create_id = res_ans_obj.create(cr, uid, {'response_id':resp_id, 'answer_id':key1.split('_')[-1], 'answer' : val1})
                            sur_name_read['store_ans'][resp_id].update({key1:val1})
                            select_count += 1
                        surv_name_wiz.write(cr, uid, [context.get('sur_name_id',False)], {'store_ans':sur_name_read['store_ans']})

                    for key,val in vals.items():
                        if val and key.split('_')[1] == "commentcolumn" and key.split('_')[0] == que_id:
                            for res_id in response_list:
                                if key.split('_')[2] in res_id.split('_')[1]:
                                    a = res_ans_obj.write(cr, uid, [res_id.split('_')[0]], {'comment_field':val})
                                    sur_name_read['store_ans'][resp_id].update({key:val})

                    if comment_field and comment_value:
                        for res in resp_id_list:
                            sur_name_read['store_ans'].pop(res)
                        raise osv.except_osv(_('Warning !'), "'" + que_rec['question']  + "' " + tools.ustr(que_rec['make_comment_field_err_msg']))

                    if que_rec['type'] == "rating_scale" and que_rec['rating_allow_one_column_require'] and len(selected_value) > len(list(set(selected_value))):
                        for res in resp_id_list:
                            sur_name_read['store_ans'].pop(res)
                        raise osv.except_osv(_('Warning !'), "'" + que_rec['question'] + "'\n" + _("You cannot select the same answer more than one time"))

                    if not select_count:
                        resp_obj.write(cr, uid, resp_id, {'state':'skip'})

                    if que_rec['numeric_required_sum'] and numeric_sum > que_rec['numeric_required_sum']:
                        for res in resp_id_list:
                            sur_name_read['store_ans'].pop(res)
                        raise osv.except_osv(_('Warning !'), "'" + que_rec['question'] + "' " + tools.ustr(que_rec['numeric_required_sum_err_msg']))

                    if que_rec['type'] in ['multiple_textboxes_diff_type', 'multiple_choice_multiple_ans','matrix_of_choices_only_one_ans','matrix_of_choices_only_multi_ans','matrix_of_drop_down_menus','rating_scale','multiple_textboxes','numerical_textboxes','date','date_and_time'] and que_rec['is_require_answer']:
                        if matrix_list:
                            if (que_rec['required_type'] == 'all' and len(list(set(matrix_list))) < len(que_rec['answer_choice_ids'])) or \
                            (que_rec['required_type'] == 'at least' and len(list(set(matrix_list))) < que_rec['req_ans']) or \
                            (que_rec['required_type'] == 'at most' and len(list(set(matrix_list))) > que_rec['req_ans']) or \
                            (que_rec['required_type'] == 'exactly' and len(list(set(matrix_list))) != que_rec['req_ans']) or \
                            (que_rec['required_type'] == 'a range' and (len(list(set(matrix_list))) < que_rec['minimum_req_ans'] or len(list(set(matrix_list))) > que_rec['maximum_req_ans'])):
                                for res in resp_id_list:
                                    sur_name_read['store_ans'].pop(res)
                                raise osv.except_osv(_('Warning !'), "'" + que_rec['question'] + "' " + tools.ustr(que_rec['req_error_msg']))

                        elif (que_rec['required_type'] == 'all' and select_count < len(que_rec['answer_choice_ids'])) or \
                            (que_rec['required_type'] == 'at least' and select_count < que_rec['req_ans']) or \
                            (que_rec['required_type'] == 'at most' and select_count > que_rec['req_ans']) or \
                            (que_rec['required_type'] == 'exactly' and select_count != que_rec['req_ans']) or \
                            (que_rec['required_type'] == 'a range' and (select_count < que_rec['minimum_req_ans'] or select_count > que_rec['maximum_req_ans'])):
                            for res in resp_id_list:
                                sur_name_read['store_ans'].pop(res)
                            raise osv.except_osv(_('Warning !'), "'" + que_rec['question'] + "' " + tools.ustr(que_rec['req_error_msg']))

                    if que_rec['type'] in ['multiple_choice_only_one_ans','single_textbox','comment'] and  que_rec['is_require_answer'] and select_count <= 0:
                        for res in resp_id_list:
                            sur_name_read['store_ans'].pop(res)
                        raise osv.except_osv(_('Warning !'), "'" + que_rec['question'] + "' " + tools.ustr(que_rec['req_error_msg']))

        else:
            resp_id_list = []
            for update in click_update:
                que_rec = que_obj.read(cr, uid , [int(sur_name_read['store_ans'][update]['question_id'])], [])[0]
                res_ans_obj.unlink(cr, uid,res_ans_obj.search(cr, uid, [('response_id', '=', update)]))
                surv_tbl_column_obj.unlink(cr, uid,surv_tbl_column_obj.search(cr, uid, [('response_table_id', '=', update)]))
                resp_id_list.append(update)
                sur_name_read['store_ans'].update({update:{'question_id':sur_name_read['store_ans'][update]['question_id']}})
                surv_name_wiz.write(cr, uid, [context.get('sur_name_id',False)], {'store_ans':sur_name_read['store_ans']})
                select_count = 0
                numeric_sum = 0
                selected_value = []
                matrix_list = []
                comment_field = False
                comment_value = False
                response_list = []

                for key, val in vals.items():
                    ans_id_len = key.split('_')
                    if ans_id_len[0] == sur_name_read['store_ans'][update]['question_id']:
                        if val and key.split('_')[1] == "table":
                            surv_tbl_column_obj.create(cr, uid, {'response_table_id' : update,'column_id':key.split('_')[2], 'name':key.split('_')[3], 'value' : val})
                            sur_name_read['store_ans'][update].update({key:val})
                            resp_obj.write(cr, uid, update, {'state': 'done'})

                        elif val and key.split('_')[1] == "otherfield" :
                            comment_field = True
                            sur_name_read['store_ans'][update].update({key:val})
                            select_count += 1
                            surv_name_wiz.write(cr, uid, [context.get('sur_name_id',False)], {'store_ans':sur_name_read['store_ans']})
                            continue

                        elif val and key.split('_')[1] == "selection":
                            if len(key.split('_')) > 2:
                                ans_create_id = res_ans_obj.create(cr, uid, {'response_id':update, 'answer_id':key.split('_')[-1], 'column_id' : val})
                                selected_value.append(val)
                                response_list.append(str(ans_create_id) + "_" + str(key.split('_')[-1]))
                            else:
                                ans_create_id = res_ans_obj.create(cr, uid, {'response_id':update, 'answer_id': val})
                            resp_obj.write(cr, uid, update, {'state': 'done'})
                            sur_name_read['store_ans'][update].update({key:val})
                            select_count += 1

                        elif key.split('_')[1] == "other":
                            if not val:
                                comment_value = True
                            else:
                                error = False
                                if que_rec['is_comment_require'] and  que_rec['comment_valid_type'] == 'must_be_specific_length':
                                    if (not val and  que_rec['comment_minimum_no']) or len(val) <  que_rec['comment_minimum_no'] or len(val) > que_rec['comment_maximum_no']:
                                        error = True
                                elif que_rec['is_comment_require'] and  que_rec['comment_valid_type'] in ['must_be_whole_number', 'must_be_decimal_number', 'must_be_date']:
                                    try:
                                        if que_rec['comment_valid_type'] == 'must_be_whole_number':
                                            value = int(val)
                                            if value <  que_rec['comment_minimum_no'] or value > que_rec['comment_maximum_no']:
                                                error = True
                                        elif que_rec['comment_valid_type'] == 'must_be_decimal_number':
                                            value = float(val)
                                            if value <  que_rec['comment_minimum_float'] or value > que_rec['comment_maximum_float']:
                                                error = True
                                        elif que_rec['comment_valid_type'] == 'must_be_date':
                                            value = datetime.datetime.strptime(val, "%Y-%m-%d")
                                            if value <  datetime.datetime.strptime(que_rec['comment_minimum_date'], "%Y-%m-%d") or value >  datetime.datetime.strptime(que_rec['comment_maximum_date'], "%Y-%m-%d"):
                                                error = True
                                    except:
                                        error = True
                                elif que_rec['is_comment_require'] and  que_rec['comment_valid_type'] == 'must_be_email_address':
                                    import re
                                    if re.match("^[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$", val) == None:
                                            error = True
                                if error:
                                    raise osv.except_osv(_('Warning !'), "'" + que_rec['question'] + "'  \n" + tools.ustr(que_rec['comment_valid_err_msg']))
                                resp_obj.write(cr, uid, update, {'comment':val,'state': 'done'})
                                sur_name_read['store_ans'][update].update({key:val})

                        elif val and key.split('_')[1] == "comment":
                            resp_obj.write(cr, uid, update, {'comment':val,'state': 'done'})
                            sur_name_read['store_ans'][update].update({key:val})
                            select_count += 1

                        elif val and (key.split('_')[1] == "single"  or (len(key.split('_')) > 2 and key.split('_')[2] == 'multi')):
                            error = False
                            if que_rec['is_validation_require'] and que_rec['validation_type'] == 'must_be_specific_length':
                                if (not val and  que_rec['validation_minimum_no']) or len(val) <  que_rec['validation_minimum_no'] or len(val) > que_rec['validation_maximum_no']:
                                    error = True
                            elif que_rec['is_validation_require'] and que_rec['validation_type'] in ['must_be_whole_number', 'must_be_decimal_number', 'must_be_date']:
                                error = False
                                try:
                                    if que_rec['validation_type'] == 'must_be_whole_number':
                                        value = int(val)
                                        if value <  que_rec['validation_minimum_no'] or value > que_rec['validation_maximum_no']:
                                            error = True
                                    elif que_rec['validation_type'] == 'must_be_decimal_number':
                                        value = float(val)
                                        if value <  que_rec['validation_minimum_float'] or value > que_rec['validation_maximum_float']:
                                            error = True
                                    elif que_rec['validation_type'] == 'must_be_date':
                                        value = datetime.datetime.strptime(val, "%Y-%m-%d")
                                        if value <  datetime.datetime.strptime(que_rec['validation_minimum_date'], "%Y-%m-%d") or value >  datetime.datetime.strptime(que_rec['validation_maximum_date'], "%Y-%m-%d"):
                                            error = True
                                except Exception ,e:
                                    error = True
                            elif que_rec['is_validation_require'] and  que_rec['validation_type'] == 'must_be_email_address':
                                import re
                                if re.match("^[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$", val) == None:
                                        error = True
                            if error:
                                raise osv.except_osv(_('Warning !'), "'" + que_rec['question'] + "'  \n" + tools.ustr(que_rec['validation_valid_err_msg']))
                            if key.split('_')[1] == "single" :
                                resp_obj.write(cr, uid, update, {'single_text':val,'state': 'done'})
                            else:
                                resp_obj.write(cr, uid, update, {'state': 'done'})
                                ans_create_id = res_ans_obj.create(cr, uid, {'response_id':update, 'answer_id':ans_id_len[1], 'answer' : val})
                            sur_name_read['store_ans'][update].update({key:val})
                            select_count += 1

                        elif val and len(key.split('_')) > 2 and key.split('_')[2] == 'numeric':
                            if not val=="0":
                                try:
                                    numeric_sum += int(val)
                                    resp_obj.write(cr, uid, update, {'state': 'done'})
                                    ans_create_id = res_ans_obj.create(cr, uid, {'response_id': update, 'answer_id':ans_id_len[1], 'answer' : val})
                                    sur_name_read['store_ans'][update].update({key:val})
                                    select_count += 1
                                except:
                                    raise osv.except_osv(_('Warning !'), "'" + que_rec['question'] + "'\n" + _("Please enter an integer value"))

                        elif val and len(key.split('_')) == 3:
                            resp_obj.write(cr, uid, update, {'state': 'done'})
                            if type(val) == type('') or type(val) == type(u''):
                                ans_create_id = res_ans_obj.create(cr, uid, {'response_id': update, 'answer_id':ans_id_len[1], 'column_id' : ans_id_len[2], 'value_choice' : val})
                                sur_name_read['store_ans'][update].update({key:val})
                            else:
                                ans_create_id = res_ans_obj.create(cr, uid, {'response_id': update, 'answer_id':ans_id_len[1], 'column_id' : ans_id_len[2]})
                                sur_name_read['store_ans'][update].update({key:True})
                            matrix_list.append(key.split('_')[0] + '_' + key.split('_')[1])
                            select_count += 1

                        elif val and len(key.split('_')) == 2:
                            resp_obj.write(cr, uid, update, {'state': 'done'})
                            ans_create_id = res_ans_obj.create(cr, uid, {'response_id': update, 'answer_id':ans_id_len[-1], 'answer' : val})
                            sur_name_read['store_ans'][update].update({key:val})
                            select_count += 1
                        surv_name_wiz.write(cr, uid, [context.get('sur_name_id',False)], {'store_ans': sur_name_read['store_ans']})

                for key,val in vals.items():
                    if val and key.split('_')[1] == "commentcolumn" and key.split('_')[0] == sur_name_read['store_ans'][update]['question_id']:
                        for res_id in response_list:
                            if key.split('_')[2] in res_id.split('_')[1]:
                                a = res_ans_obj.write(cr, uid, [res_id.split('_')[0]], {'comment_field':val})
                                sur_name_read['store_ans'][update].update({key:val})

                if comment_field and comment_value:
                    raise osv.except_osv(_('Warning !'), "'" + que_rec['question']  + "' " + tools.ustr(que_rec['make_comment_field_err_msg']))

                if que_rec['type'] == "rating_scale" and que_rec['rating_allow_one_column_require'] and len(selected_value) > len(list(set(selected_value))):
                    raise osv.except_osv(_('Warning !'), "'" + que_rec['question'] + "\n" + _("You cannot select same answer more than one time'"))

                if que_rec['numeric_required_sum'] and numeric_sum > que_rec['numeric_required_sum']:
                    raise osv.except_osv(_('Warning !'), "'" + que_rec['question'] + "' " + tools.ustr(que_rec['numeric_required_sum_err_msg']))

                if not select_count:
                    resp_obj.write(cr, uid, update, {'state': 'skip'})

                if que_rec['type'] in ['multiple_textboxes_diff_type','multiple_choice_multiple_ans','matrix_of_choices_only_one_ans','matrix_of_choices_only_multi_ans','matrix_of_drop_down_menus','rating_scale','multiple_textboxes','numerical_textboxes','date','date_and_time'] and que_rec['is_require_answer']:
                    if matrix_list:
                        if (que_rec['required_type'] == 'all' and len(list(set(matrix_list))) < len(que_rec['answer_choice_ids'])) or \
                        (que_rec['required_type'] == 'at least' and len(list(set(matrix_list))) < que_rec['req_ans']) or \
                        (que_rec['required_type'] == 'at most' and len(list(set(matrix_list))) > que_rec['req_ans']) or \
                        (que_rec['required_type'] == 'exactly' and len(list(set(matrix_list))) != que_rec['req_ans']) or \
                        (que_rec['required_type'] == 'a range' and (len(list(set(matrix_list))) < que_rec['minimum_req_ans'] or len(list(set(matrix_list))) > que_rec['maximum_req_ans'])):
                            raise osv.except_osv(_('Warning !'), "'" + que_rec['question'] + "' " + tools.ustr(que_rec['req_error_msg']))

                    elif (que_rec['required_type'] == 'all' and select_count < len(que_rec['answer_choice_ids'])) or \
                        (que_rec['required_type'] == 'at least' and select_count < que_rec['req_ans']) or \
                        (que_rec['required_type'] == 'at most' and select_count > que_rec['req_ans']) or \
                        (que_rec['required_type'] == 'exactly' and select_count != que_rec['req_ans']) or \
                        (que_rec['required_type'] == 'a range' and (select_count < que_rec['minimum_req_ans'] or select_count > que_rec['maximum_req_ans'])):
                            raise osv.except_osv(_('Warning !'), "'" + que_rec['question'] + "' " + tools.ustr(que_rec['req_error_msg']))

                if que_rec['type'] in ['multiple_choice_only_one_ans','single_textbox','comment'] and  que_rec['is_require_answer'] and select_count <= 0:
                    raise osv.except_osv(_('Warning !'), "'" + que_rec['question'] + "' " + tools.ustr(que_rec['req_error_msg']))
            
        return True
survey_question_wiz()