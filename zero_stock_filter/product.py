# -*- coding: utf-8 -*-
###############################################################################~!!~~!!!
#
# Copyright (c) 2010-2012, OPENTIA Group (<http://opentia.com>)
# The word "OPENTIA" is an European Community Trademark property of the Opentia Group
#
# @author: Opentia "Happy Hacking" Team
# @e-mail: consultoria@opentia·es
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
###############################################################################~!!~~!!!
from osv import fields,osv
from tools.translate import _
import decimal_precision as dp


class product_product(osv.osv):
    _inherit = "product.product"

    def _get_product_available_func(states, what):
        def _product_available(self, cr, uid, ids, name, arg, context=None):
            return {}.fromkeys(ids, 0.0)
        return _product_available

    _product_virtual_available = _get_product_available_func(('confirmed','waiting','assigned','done'), ('in', 'out'))

    def _product_available(self, cr, uid, ids, field_names=None, arg=False, context=None):
        return super(product_product,self)._product_available(cr, uid, ids, field_names=field_names, arg=arg, context=context)

    def _virtual_available_search(self, cr, uid, obj, name, args, context=None):
        ops = ['>',]
        prod_ids = ()
        if not len(args):
            return []
        prod_ids = []
        for a in args:
            operator = a[1]
            value = a[2]
#            if not operator in ops:
#                raise osv.except_osv(_('Error !'), _('Operator %s not suported in searches for virtual_available (product.product).' % operator))
#            if operator == '>':
            todos = self.search(cr, uid, [])
            ids = self.read(cr, uid, todos, ['virtual_available'], context=context)
            for d in ids:
                if operator =='>':
                    if d['virtual_available'] > value:
                        prod_ids.append(d['id'])
                elif operator =='>=':
                    if d['virtual_available'] >= value:
                        prod_ids.append(d['id'])
                elif operator =='<':
                    if d['virtual_available'] < value:
                        prod_ids.append(d['id'])
                elif operator =='<=':
                    if d['virtual_available'] <= value:
                        prod_ids.append(d['id'])
                elif operator =='==' or operator =='=':
                    if d['virtual_available'] == value:
                        prod_ids.append(d['id'])
        return [('id','in',tuple(prod_ids))]

    _columns = {
        'virtual_available': fields.function(_product_available, fnct_search=_virtual_available_search, method=True, type='float', string='Virtual Stock', help="Future stock for this product according to the selected locations or all internal if none have been selected. Computed as: Real Stock - Outgoing + Incoming.", multi='qty_available', digits_compute=dp.get_precision('Product UoM')),
    }

product_product()
