# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time
from lxml import etree
import decimal_precision as dp

import netsvc
import pooler
from osv import fields, osv, orm
from tools.translate import _

class account_analytic_account(osv.osv):
    _inherit = 'account.analytic.account'
    
    def name_get(self, cr, uid, ids, context=None):
        if not ids:
            return []
        res = []
        for account in self.browse(cr, uid, ids, context=context):
            if account.code:
                res.append((account.id, account.code))
            else:
                data = []
                acc = account
                while acc:
                    data.insert(0, acc.name)
                    acc = acc.parent_id
                data = ' / '.join(data)
                res.append((account.id, data))
        return res
    def name_get2(self, cr, uid, ids, context=None):
        if not ids:
            return []
        res = []
        for account in self.browse(cr, uid, ids, context=context):
            
            data = []
            acc = account
            while acc:
                data.insert(0, acc.name)
                acc = acc.parent_id
            data = ' / '.join(data)
            res.append((account.id, data))
        return res
    def name_search(self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []
        if context is None:
            context = {}
        
        args = args[:]
#        if context.get('current_model') == 'project.project':
#            cr.execute("select analytic_account_id from project_project ")
#            project_ids = [x[0] for x in cr.fetchall()]
#            # We cannot return here with normal project_ids, the following process also has to be followed.
#            # The search should consider the name inhere, earlier it was just bypassing it.
#            # Hence, we added the args and let the below mentioned procedure do the trick
#            # Let the search method manage this.
#            args += [('id', 'in', project_ids)]
#            return self.name_get(cr, uid, project_ids, context=context)
        account = self.search(cr, uid, [('code', 'ilike', '%%%s%%' % name)]+args, limit=limit, context=context)
        if not account:
            account = self.search(cr, uid, [('name', 'ilike', '%%%s%%' % name)]+args, limit=limit, context=context)
            newacc = account
            while newacc:
                newacc = self.search(cr, uid, [('parent_id', 'in', newacc)]+args, limit=limit, context=context)
                account += newacc

        return self.name_get(cr, uid, account, context=context)
    
    
    def _complete_name_calc(self, cr, uid, ids, prop, unknow_none, unknow_dict):
        res = self.name_get2(cr, uid, ids)
        return dict(res)
    
    _columns = {'complete_name': fields.function(_complete_name_calc, method=True, type='char', string='Full Account Name'),
                 }
account_analytic_account()