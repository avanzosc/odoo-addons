# -*- encoding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

from openerp.osv import orm, fields


class sale_order(orm.Model):

    _inherit = 'sale.order'

    _columns = {
        'tax_apportionment_ids': fields.one2many('tax.apportionment',
                                                 'sale_id',
                                                 'Tax Apportionment'),
    }

    def _calc_apportionment_taxes(self, cr, uid, ids, context=None):
        if not context:
            context = {}

        apport_obj = self.pool['tax.apportionment']
        cur_obj = self.pool['res.currency']

        for order in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, order.id,
                       {'tax_apportionment_ids': [(6, 0, [])]})

            for line in order.order_line:
                cur = line.order_id.pricelist_id.currency_id
                for tax in line.tax_id:
                    apport_ids = apport_obj.search(cr, uid,
                                                   [('sale_id', '=', order.id),
                                                    ('tax_id', '=', tax.id)])
                    if not apport_ids:
                        line_vals = {
                            'sale_id': order.id,
                            'tax_id': tax.id,
                            'untaxed_amount':
                            cur_obj.round(cr, uid, cur, line.price_subtotal),
                            'taxation_amount':
                            cur_obj.round(cr, uid, cur,
                                          (line.price_subtotal * tax.amount)),
                            'total_amount':
                            cur_obj.round(cr, uid, cur,
                                          (line.price_subtotal *
                                           (1 + tax.amount)))
                        }
                        apport_obj.create(cr, uid, line_vals)
                    else:
                        apport = apport_obj.browse(cr, uid, apport_ids[0])
                        untaxed_amount = cur_obj.round(
                            cr, uid, cur,
                            line.price_subtotal + apport.untaxed_amount)
                        taxation_amount = cur_obj.round(
                            cr, uid, cur, untaxed_amount * tax.amount)
                        total_amount = cur_obj.round(
                            cr, uid, cur, untaxed_amount + taxation_amount)
                        apport_obj.write(cr, uid, [apport.id],
                                         {'untaxed_amount': untaxed_amount,
                                          'taxation_amount': taxation_amount,
                                          'total_amount': total_amount})

        return True

    def action_wait(self, cr, uid, ids, context=None):
        if not context:
            context = {}

        self._calc_apportionment_taxes(cr, uid, ids, context=context)

        return super(sale_order, self).action_wait(cr, uid, ids, context)

    def button_dummy(self, cr, uid, ids, context=None):

        super(sale_order, self).button_dummy(cr, uid, ids, context=context)

        if ids:
            self._calc_apportionment_taxes(cr, uid, ids, context=context)

        return True
