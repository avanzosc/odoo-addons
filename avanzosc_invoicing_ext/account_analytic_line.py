# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc - Advanced Open Source Consulting
#    Copyright (C) 2011 - 2013 Avanzosc <http://www.avanzosc.com>
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

from osv import osv
from osv import fields

class account_analytic_line(osv.osv):
    
    _name = 'account.analytic.line'
    _inherit = 'account.analytic.line'
    
    def create(self, cr, uid, values, context=None):
        agreement_obj = self.pool.get('inv.agreement')
        res = super(account_analytic_line, self).create(cr, uid, values, context)
        if values.has_key('agr_id'):
            if values['agr_id']:
                agreement = agreement_obj.browse(cr,uid,values['agr_id'])
                if agreement.period_qty > 0:
                    vals = {}
                    if agreement.period_qty == 1:
                        vals.update({'fixed_price': agreement.fixed_price_extra, 'period_qty':0})
                    elif agreement.period_qty > 1:
                        vals.update({'period_qty': (agreement.period_qty -1)}) 
                    if vals:
                        agreement_obj.write(cr,uid,[agreement.id], vals)
        return res
account_analytic_line()