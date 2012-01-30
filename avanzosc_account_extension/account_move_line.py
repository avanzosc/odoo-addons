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
from datetime import datetime
from operator import itemgetter

import netsvc
from osv import fields, osv
from tools.translate import _
import decimal_precision as dp
import tools

class account_move_line(osv.osv):
    
    _inherit = 'account.move.line'
    
    def _default_get(self, cr, uid, fields, context=None):
        res = {}
        journal_obj = self.pool.get('account.journal')
        res = super(account_move_line, self)._default_get(cr, uid, fields, context=context)
        if res:
            if res.has_key('journal_id'):
                journal = journal_obj.browse(cr,uid,[res['journal_id']])
                if journal:
                    journal = journal[0]
                    acc = False
                    if journal.default_debit_account_id:
                        acc = journal.default_debit_account_id.id
                    elif journal.default_credit_account_id:
                        acc = journal.default_debit_account_id.id
                    res['account_id'] = acc
            res['name'] = False
        return res
    
    def unlink(self, cr, uid, ids, context=None, check=True):
            a_line_obj = self.pool.get('account.analytic.line')
            if context is None:
                context = {}
            move_obj = self.pool.get('account.move')
            self._update_check(cr, uid, ids, context)
            result = False
            for line in self.browse(cr, uid, ids, context=context):
                a_line_list = a_line_obj.search(cr,uid,[('move_id', '=', line.id)], context=context)
                if a_line_list:
                    a_line_obj.unlink(cr,uid,a_line_list, context=context)
                context['journal_id'] = line.journal_id.id
                context['period_id'] = line.period_id.id
                result = super(account_move_line, self).unlink(cr, uid, [line.id], context=context)
                if check:
                    move_obj.validate(cr, uid, [line.move_id.id], context=context)
            return result
        
account_move_line()