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

from osv import fields, osv

class res_partner(osv.osv):
    
    _inherit='res.partner'
    _name='res.partner'


    def _new_credit_get(self, cr, uid, ids, field_names, arg, context=None):
        res = {}
        property_obj = self.pool.get('ir.property')
        account_obj = self.pool.get('account.account')
        for part_o in self.browse(cr,uid,ids):
            account_list = property_obj.search(cr,uid,[('name','=','property_account_receivable'),('value_reference','!=',False),('res_id','=','res.partner,'+str(part_o.id)+'')])
            account_balance = 0.0
            if account_list:
                account_list_o = property_obj.browse(cr,uid, account_list[0])
                account_balance = account_obj.browse(cr,uid,account_list_o.value_reference.id).balance
            res[part_o.id] = account_balance
        return res
    
    def _new_debit_get(self, cr, uid, ids, field_names, arg, context=None): 
        res = {}
        property_obj = self.pool.get('ir.property')
        account_obj = self.pool.get('account.account')
        for part_o in self.browse(cr,uid,ids):
            account_list = property_obj.search(cr,uid,[('name','=','property_account_payable'),('value_reference','!=',False),('res_id','=','res.partner,'+str(part_o.id)+'')])
            account_balance = 0.0
            if account_list:
                account_list_o = property_obj.browse(cr,uid, account_list[0])
                account_balance = account_obj.browse(cr,uid,account_list_o.value_reference.id).balance
            res[part_o.id] = account_balance
        return res
        
        
    _columns ={
               'new_credit':fields.function(_new_credit_get, method=True, type='float',string='Customer Balance', store=False),
               'new_debit':fields.function(_new_debit_get, method=True, type='float', string='Supplier Balance', store=False),
               
               }

res_partner()