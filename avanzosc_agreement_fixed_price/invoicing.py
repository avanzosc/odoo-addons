# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc - Avanced Open Source Consulting
#    Copyright (C) 2010 - 2011 Avanzosc <http://www.avanzosc.com>
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

from osv import fields,osv
import netsvc
import tools
import re
from tools.translate import _
from mx import DateTime
from mx.DateTime import now
import time, locale
import traceback, sys

def _change_state(self, cr, uid, ids, field, field_type, field_id, value1_char, value1_bool, \
        value1_int, value2_int, value1_float, value2_float, value1_date, value2_date, value1_datetime, value2_datetime, cond_value):
    data = {}
    if field_id:
        field_name = self.pool.get('ir.model.fields').browse(cr, uid, field_id, {}).name
    else:
        field_name = 'count'
    if not field:
        return {'value':{},'state':False}
    else:
        cond_type = self.pool.get('inv.rec_type').browse(cr, uid, field).value
        data['state'] = self.pool.get('inv.rec_type').browse(cr, uid, field).type
        value = self.pool.get('inv.rec_type').browse(cr, uid, field).value
        if data['state']!='[many2one]' and data['state']!='[one2many]' and data['state']!='[many2many]' and data['state']!='[boolean]' \
                and data['state']!='[char]' and data['state']!='[selection]':
            if value=='between' or value=='not between':
                data['state'] += '|2|'
            else:
                data['state'] += '|1|'
        if value!='between' and value!='not between':
            data['value2_int'] = 0
            data['value2_float'] = 0
            data['value2_date'] = ''
            data['value2_datetime'] = ''

        res = ''
        if cond_type == 'equal to':
            operator = ' == '
        elif cond_type == 'not equal to':
            operator = ' != '
        elif cond_type == 'greater than':
            operator = ' > '
        elif cond_type == 'less than':
            operator = ' < '
        elif cond_type == 'greater than or equal to':
            operator = ' >= '
        elif cond_type == 'less than or equal to':
            operator = ' <= '
        elif cond_type == 'regexp':
            operator = ' match '
        else:
            operator = ''

        if cond_type!='between' and cond_type!='not between':
            if field_type == '[char]' or field_type == '[selection]':
                res = field_name + operator + "'"+(value1_char and unicode(value1_char, "UTF-8") or '')+"'" or ''
            elif field_type == '[boolean]':
                res = field_name + operator + str(value1_bool) or ''
            elif field_type == '[integer]':
                res = field_name + operator + str(value1_int) or ''
            elif field_type == '[float]':
                res = field_name + operator + str(value1_float) or ''
            elif field_type == '[date]':
                res = field_name + operator + str(value1_date) or ''
            elif field_type == '[datetime]':
                res = field_name + operator + str(value1_datetime) or ''
        elif cond_type=='between':
            if field_type == '[integer]':
                res = '(' + field_name + ' >= ' + str(value1_int)+')'
                if value2_int != None:
                    res += ' and ('+field_name+ ' <= ' + str(value2_int)+')' or ''
            elif field_type == '[float]':
                res = '(' + field_name + ' >= ' + str(value1_float)+')'
                if value2_float != None:
                    res += ' and ('+field_name+ ' <= ' + str(value2_float)+')' or ''
            elif field_type == '[date]':
                res = '(' + field_name + ' >= ' + str(value1_date)+')'
                if value2_date:
                    res += ' and ('+field_name+ ' <= ' + str(value2_date)+')' or ''
            elif field_type == '[datetime]':
                res += '(' + field_name + ' >= ' + str(value1_datetime)+')'
                if value2_datetime:
                    res += ' and ('+field_name+ ' <= ' + str(value2_datetime)+')' or ''
        elif cond_type=='not between':
            if field_type == '[integer]':
                res = '(' + field_name + ' <= ' + str(value1_int)+')' or ''
                if value2_int != None:
                    res += ' and ('+field_name+ ' >= ' + str(value2_int)+')' or ''
            elif field_type == '[float]':
                res = '(' + field_name + ' <= ' + str(value1_float)+')'
                if value2_float != None:
                    res += ' and ('+field_name+ ' >= ' + str(value2_float)+')' or ''
            elif field_type == '[date]':
                res = '(' + field_name + ' <= \'' + str(value1_date)+'\')'
                if value2_date:
                    res += ' and ('+field_name+ ' >= \'' + str(value2_date)+'\')' or ''
            elif field_type == '[datetime]':
                res = '(' + field_name + ' <= \'' + str(value1_datetime)+'\')'
                if value2_datetime:
                    res += ' and ('+field_name+ ' >= \'' + str(value2_datetime)+'\')' or ''

        if cond_type=='in' or cond_type=='not in':
            res = field_name + ' ' + cond_type
            if cond_value and cond_value != None:
                res += ' ['+cond_value+']' or ''
        data['name'] = res
    return data

#def convert_date(self, date):
#    return time.strftime(locale.nl_langinfo(locale.D_FMT), time.strptime(date, '%Y-%m-%d'))

def convert_date(self, date):
    if len(date)==10:
        return date[8:10]+'.'+date[5:7]+'.'+date[:4]+'.'
    elif len(date)==7:
        return date[5:7]+'.'+date[:4]+'.'
    return date+'.'

def reconvert_date(self, date):
    try:
        if len(date)==11:
            retval = date[6:10]+'-'+date[3:5]+'-'+date[:2]
            DateTime.strptime(retval, '%Y-%m-%d')
            return retval
        elif len(date)==8:
            retval = date[3:7]+'-'+date[:2]+'-01'
            DateTime.strptime(retval, '%Y-%m-%d')
            return retval
        else:
            retval = date[:4]+'-01-01'
            DateTime.strptime(retval, '%Y-%m-%d')
            return retval
    except Exception, e:
        return '1900-01-01'

def find_req_users(self, cr, uid, service):
    result = []
    admin_id = self.pool.get('res.users').search(cr, uid, [('login','=','admin')])[0]
    srv = self.pool.get('inv.service').browse(cr, uid, service, {})
    tgroup = map(int, srv.req_users)
    #Structure changes in 6.0. Commented 5 lines
    #tg_obj = self.pool.get('hr.timesheet.group')
    #for wt in tgroup:
    #    user = tg_obj.browse(cr, uid, wt, {}).manager.id
    #    if user not in result:
    #        result.append(user)

    tg_obj = self.pool.get('hr.employee')
    wts = tg_obj.search(cr, uid, [('user_id', 'in', tgroup)])
    for emp in tg_obj.browse(cr, uid, wts, {}):
        if emp.department_id:
            if emp.department_id.manager_id and emp.id == emp.department_id.manager_id.id:
                user = emp.department_id.manager_id.id
                if user not in result:
                    result.append(user)
    #emp_obj = self.pool.get('hr.employee')
    #emp_ids = emp_obj.search(cr, uid, [])
    #for id in emp_ids:
    #    emp_rec = emp_obj.browse(cr, uid, id, {})
    #    for r in map(int, srv.req_users):
    #        if r in map(int, emp_rec.workgroups):
    #            user = emp_rec.user_id.id
    #            if user not in result:
    #                result.append(emp_rec.user_id.id)
    if result and result[0]:
        return result
    else:
        return [admin_id]

def create_request(self, cr, uid, subject, req_text, service):
    req_users = find_req_users(self, cr, uid, service)
    admin_id = self.pool.get('res.users').search(cr, uid, [('login','=','admin')])[0]
    for user_id in req_users:
        req_values = {'name':subject,'act_from':admin_id,'act_to':user_id,'date_sent':time.strftime('%Y-%m-%d %H:%M:%S'),'body':req_text,'state':'waiting','priority':'2'}
        id = self.pool.get('res.request').create(cr, uid, req_values)
        cr.execute('select act_from,act_to,body,date_sent from res_request where id=%s', (id,))
        values = cr.dictfetchone()
        if len(values['body']) > 128:
            values['name'] = values['body'][:125] + '...'
        else:
            values['name'] = values['body'] or '/'
        values['req_id'] = id
        self.pool.get('res.request.history').create(cr, uid, values)
    return True

class method(osv.osv):
    _inherit = 'inv.method'
 
    def _run_filters(self, cr, uid, ids, agr_id, context={}):
        acc_lines = []
        agr = self.pool.get('inv.agreement')
        r = agr.browse(cr, uid, agr_id, {})
        d_list = self.pool.get('inv.date_list')
        current_date = now().strftime('%Y-%m-%d')
        if r.service.invoicing == 'period':
            full_date_list = map(int, r.date_list)
            date_list1 = d_list.search(cr, uid, [('id','in',full_date_list),('status','=','wait')])
            date_list2 = d_list.search(cr, uid, [('id','in',full_date_list),('status','=','process')])
            date_list = date_list2 + date_list1
            if not date_list: return True
            date_list.reverse()
            date_id = date_list.pop()
            date = d_list.browse(cr, uid, date_id, {}).date
            pdate1 = DateTime.strptime(d_list.browse(cr, uid, date_id, {}).pdate1, '%Y-%m-%d')
            pdate2 = DateTime.strptime(d_list.browse(cr, uid, date_id, {}).pdate2, '%Y-%m-%d')
        else:
            date = current_date
            date_id = False
            pdate1 = False
            pdate2 = False
            date_list = []
        try:
            if date <= current_date and r.service.invoicing=='period':
                d_list.write(cr, uid, date_id, {'status':'process'})
            for p in self.browse(cr, uid, ids, {}):
                mas_after = []
                localspace = {"self":self,"cr":cr,"uid":uid,"re":re,"mas_aft":mas_after,"partner_id":r.partner_id.id,"contact_ids":map(int, r.partner_id.address),"pdate1":pdate1,"pdate2":pdate2,"invoice_date":date,"agre":r}
                exec p.source in localspace
                mas_after = localspace['mas_aft']
                if len(mas_after) > 0:
                    calc_ids = map(int, p.calc_ids)
                    calc_seq = self.sort_calc_list(cr, uid, calc_ids)
                    calc_res = False
                    for c_id in calc_seq:
                        c = self.pool.get('inv.calc').browse(cr, uid, c_id, {})
                        #if c.var == 'count':
                        calc_localspace = {"self":self,"cr":cr,"uid":uid,"re":re,"obj_ids":mas_after,"count":len(mas_after),"pdate1":pdate1,"pdate2":pdate2,"calc_date":date,"agre":r}
                        exec c.code in calc_localspace
                        pos = 0
                        for result in calc_localspace['res_list']:
                            if result:
                                calc_res = True
                                line = {"agr_id":agr_id,"user_id":uid,"amount":0}
                                # Analityc Entries, field Description
                                if c.description == 'empty':
                                    line['name'] = ' '
                                elif c.description == 'date':
                                    line['name'] = convert_date(self, current_date)
                                elif c.description == 'period':
                                    period = d_list.browse(cr, uid, date_id, {}).period
                                    line['name'] = period
                                elif c.description == 'field' and c.descr_field:
                                    line['name'] = ''
                                    rec_id = mas_after[pos]
                                    #for rec_id in mas_after:
                                    localspace = {"self":self,"cr":cr,"uid":uid,"model":p.model_id.model,"rec_id":rec_id,"pdate1":pdate1,"pdate2":pdate2,"calc_date":date,'d_list':d_list,"agre":r}
                                    cr.execute("SELECT ttype, relation FROM ir_model_fields WHERE name='"+c.descr_field.name+"' and model='"+p.model_id.model+"'")
                                    query_res = cr.fetchone()
                                    if query_res[0] == 'many2one':
                                        field_value = "ids = self.pool.get('"+p.model_id.model+"').browse(cr, uid, rec_id, {})."+c.descr_field.name+".id\n"
                                        field_value += "field_val = self.pool.get('"+query_res[1]+"').name_get(cr, uid, [ids], {})"
                                    elif query_res[0] == 'one2many' or query_res[0] == 'many2many':
                                        field_value = "ids = map(int, self.pool.get('"+p.model_id.model+"').browse(cr, uid, rec_id, {})."+c.descr_field.name+")\n"
                                        field_value += "field_val = self.pool.get('"+query_res[1]+"').name_get(cr, uid, ids, {})"
                                    else:
                                        field_value = "field_val = self.pool.get('"+p.model_id.model+"').browse(cr, uid, rec_id, {})."+c.descr_field.name
                                    exec field_value in localspace
                                    if query_res[0] == 'many2one' or query_res[0] == 'one2many' or query_res[0] == 'many2many':
                                        res = ''
                                        for n in localspace['field_val']:
                                            if n != localspace['field_val'][0]:
                                                res += '; '
                                            if n[1][0]!='(' and n[1][-1]!=')':
                                                name = "'"+n[1]+"'"
                                            else:
                                                name = n[1]
                                            temp = 'name='+name
                                            exec temp in localspace
                                            if type(localspace['name'])==tuple:
                                                res += localspace['name'][0][1]
                                            else:
                                                res += localspace['name']
                                        line['name'] += res
                                    else:
                                        line['name'] += str(localspace['field_val'])
                                    #if rec_id!=mas_after[-1] and localspace['field_val']: line['name'] += '; '

                                elif c.description == 'expression':
                                    if (c.descr_express).find('rec_id') != -1:
                                        line['name'] = ''
                                        #for rec_id in mas_after:
                                        rec_id = mas_after[pos]
                                        localspace = {"self":self,"cr":cr,"uid":uid,"model":p.model_id.model,"rec_id":rec_id,"agr_id":r.id,"meth_id":p.id,"calc_id":c.id,"desc":'','convert_date':convert_date,'now':now,'d_list':d_list,'date_id':date_id,'pdate1':pdate1,'pdate2':pdate2,"calc_date":date,"agre":r}
                                        exec c.descr_express in localspace
                                        if type(localspace['desc'])==list:
                                            for l in localspace['desc']:
                                                line['name'] += l[1]
                                                if l != localspace['desc'][-1]: line['name'] += '; '
                                        else:
                                            line['name'] += localspace['desc']
                                        #if rec_id!=mas_after[-1]: line['name'] += '; '
                                    else:
                                        rec_id = mas_after[pos]
                                        localspace = {"self":self,"cr":cr,"uid":uid,"model":p.model_id.model,"rec_id":rec_id,"agr_id":r.id,"meth_id":p.id,"calc_id":c.id,"desc":'','convert_date':convert_date,'now':now,'d_list':d_list,'date_id':date_id,'pdate1':pdate1,'pdate2':pdate2,"calc_date":date,"agre":r}
                                        exec c.descr_express in localspace
                                        line['name'] = localspace['desc']
                                else:
                                    line['name'] = ' '
                                # Analityc Entries, field Quantity
                                if c.quantity == 'eqone':
                                    line['unit_amount'] = 1
                                elif c.quantity == 'count':
                                    line['unit_amount'] = len(mas_after)
                                elif c.quantity == 'expression' or c.quantity == 'field':
                                    if (c.quantity_express).find('rec_id') != -1:
                                        line['unit_amount'] = 0
                                        rec_id = mas_after[pos]
                                        #for rec_id in mas_after:
                                        localspace = {"self":self,"cr":cr,"uid":uid,"model":p.model_id.model,"rec_id":rec_id,"agr_id":r.id,"meth_id":p.id,"calc_id":c.id,"pdate1":pdate1,"pdate2":pdate2,"calc_date":date,"agre":r,"quant":''}
                                        exec c.quantity_express in localspace
                                        if type(localspace['quant'])==list:
                                            for l in localspace['quant']:
                                                line['unit_amount'] += l[1]
                                        else:
                                            line['unit_amount'] = localspace['quant']
                                    else:
                                        rec_id = mas_after[pos]
                                        localspace = {"self":self,"cr":cr,"uid":uid,"model":p.model_id.model,"rec_id":rec_id,'mas_after':mas_after,"agr_id":r.id,"meth_id":p.id,"calc_id":c.id,"pdate1":pdate1,"pdate2":pdate2,"calc_date":date,"agre":r,"quant":''}
                                        exec c.quantity_express in localspace
                                        line['unit_amount'] = localspace['quant']
                                else:
                                    line['unit_amount'] = 0
                                # Analityc Entries, field Analytic Account
                                line['account_id'] = r.analytic_account.id
                                # Analityc Entries, field Analytic journal
                                line['journal_id'] = r.service.journal_id.id
                                # Analityc Entries, field General account
                                #if r.partner_id.property_account_receivable:
                                line['general_account_id'] = c.product_id.product_tmpl_id.property_account_expense.id or c.product_id.categ_id.property_account_expense_categ.id
                                # Analityc Entries, field Product
                                line['product_id'] = c.product_id.id
                                # Analityc Entries, field Product UoM
                                line['product_uom_id'] = c.product_id.uom_id.id
                                # Analityc Entries, field Invoicing
                                line['to_invoice'] = c.invoicing_id.id
#                                if r.service.purch_pricelist_id:
#                                    ppl = r.service.purch_pricelist_id.id
#                                    line['amount'] = -self.pool.get('product.pricelist').price_get(cr, uid, [ppl], line['product_id'], line['unit_amount'] or 1.0, r.partner_id.id)[ppl]
#                                elif r.fixed_price != 0:
                                line['sale_amount'] = r.fixed_price
#                                elif r.service.pricelist_id:
#                                    spl = r.service.pricelist_id.id
#                                    line['sale_amount'] = self.pool.get('product.pricelist').price_get(cr, uid, [spl], line['product_id'], line['unit_amount'] or 1.0, r.partner_id.id)[spl]
                                if r.service.invoicing == 'trigger':
                                    date_id = d_list.create(cr, uid, {'agreement_id':r.id,'status':'inv','date':date,'state':'filled'})
                                    line['invlog_id'] = date_id
                                    acc_lines.append(self.pool.get('account.analytic.line').create(cr, uid, line))
                                else:
                                    line['invlog_id'] = date_id
                                if date <= current_date and r.service.invoicing=='period':
                                    cr.rollback()
                                    acc_lines.append(self.pool.get('account.analytic.line').create(cr, uid, line))
                                    d_list.write(cr, uid, date_id, {'status':'inv'})
                                    cr.commit()
                            pos += 1
                    if not calc_res and date_id:
                        d_list.write(cr, uid, date_id, {'status':'error'})
                        agr.write(cr, uid, [agr_id], {'state':'error'})
                        req_body = '- Methodology: '+p.name+'\n- Calculation:\n'+c.code+'\n- Calculation result: False'
                        create_request(self, cr, uid, 'Calculation result is False', req_body, r.service.id)
        except Exception, e:
            cr.rollback()
            if date <= current_date and r.service.invoicing=='period':
                d_list.write(cr, uid, date_id, {'status':'error'})
                agr.write(cr, uid, [agr_id], {'state':'error'})
                cr.commit()
            tb_s = reduce(lambda x, y: x+y, traceback.format_exception(sys.exc_type, sys.exc_value, sys.exc_traceback))
            create_request(self, cr, uid, 'Error in executed code', tb_s, r.service.id)
        return acc_lines

method()
