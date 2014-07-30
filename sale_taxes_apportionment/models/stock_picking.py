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

from openerp.osv import orm, fields
import openerp.addons.decimal_precision as dp


class stock_picking(orm.Model):

    _inherit = 'stock.picking'

    _columns = {
        'tax_apportionment_ids': fields.one2many('tax.apportionment',
                                                 'picking_id',
                                                 'Tax Apportionment'),
    }

    def _amount_all(self, cr, uid, ids, field_name, arg, context=None):
        cur_obj = self.pool['res.currency']
        tax_obj = self.pool['account.tax']
        res = {}
        for picking in self.browse(cr, uid, ids, context=context):
            res[picking.id] = {
                'amount_untaxed': 0.0,
                'amount_total': 0.0,
            }
            val1 = val = 0.0

            for line in picking.move_lines:
                if line.procurement_id and line.procurement_id.sale_line_id:
                    sale_line = line.procurement_id.sale_line_id
                    cur = sale_line.order_id.pricelist_id.currency_id
                    price = sale_line.price_unit * (
                        1 - (sale_line.discount or 0.0) / 100.0)

                    taxes = tax_obj.compute_all(
                        cr, uid, sale_line.tax_id,
                        price, line.product_qty,
                        sale_line.order_id.partner_invoice_id.id,
                        line.product_id, sale_line.order_id.partner_id)

                    val1 += cur_obj.round(cr, uid, cur, taxes['total'])
                    val += cur_obj.round(cr, uid, cur, taxes['total_included'])

            res[picking.id]['amount_untaxed'] = val1
            res[picking.id]['amount_total'] = val
        return res

    def _get_order(self, cr, uid, ids, context=None):
        result = {}
        for move in self.pool['stock.move'].browse(cr, uid, ids,
                                                   context=context):
            result[move.picking_id.id] = True
        return result.keys()

    _columns = {
        'amount_untaxed':
        fields.function(_amount_all,
                        digits_compute=dp.get_precision('Sale Price'),
                        string='Untaxed Amount',
                        store={
                            'stock.picking': (lambda self, cr, uid, ids,
                                              c={}: ids, ['move_lines'], 10),
                            'stock.move': (_get_order,
                                           ['product_qty',
                                            'product_uos_qty'], 10),
                        },
                        multi='sums', help="The amount without tax."),
        'amount_total':
        fields.function(_amount_all,
                        digits_compute=dp.get_precision('Sale Price'),
                        string='Total',
                        store={
                            'stock.picking': (lambda self, cr, uid, ids,
                                              c={}: ids, ['move_lines'], 10),
                            'stock.move': (_get_order,
                                           ['product_qty',
                                            'product_uos_qty'], 10),
                        },
                        multi='sums', help="The total amount."),
        'tax_apportionment_ids': fields.one2many('tax.apportionment',
                                                 'picking_id',
                                                 'Tax Apportionment'),
    }

    def _calc_apportionment_taxes(self, cr, uid, ids, context=None):
        if context is None:
            context = {}

        apportion_obj = self.pool['tax.apportionment']
        tax_obj = self.pool['account.tax']
        cur_obj = self.pool['res.currency']

        for picking in self.browse(cr, uid, ids, context=context):
            for line in picking.move_lines:
                if line.procurement_id and line.procurement_id.sale_line_id:
                    sale_line = line.procurement_id.sale_line_id
                    cur = sale_line.order_id.pricelist_id.currency_id
                    for tax in sale_line.tax_id:
                        price = sale_line.price_unit * (
                            1 - (sale_line.discount or 0.0) / 100.0)
                        taxes = tax_obj.compute_all(
                            cr, uid, sale_line.tax_id,
                            price, line.product_qty,
                            sale_line.order_id.partner_invoice_id.id,
                            line.product_id,
                            sale_line.order_id.partner_id)

                        apportionment_ids = apportion_obj.search(
                            cr, uid, [('picking_id', '=', picking.id),
                                      ('tax_id', '=', tax.id)])
                        subtotal = cur_obj.round(cr, uid, cur, taxes['total'])

                        if not apportionment_ids:
                            line_vals = {
                                'picking_id': picking.id,
                                'tax_id': tax.id,
                                'untaxed_amount': subtotal,
                                'taxation_amount':
                                cur_obj.round(cr, uid, cur,
                                              (subtotal * tax.amount)),
                                'total_amount':
                                cur_obj.round(cr, uid, cur,
                                              (subtotal * (1 + tax.amount)))
                            }
                            apportion_obj.create(cr, uid, line_vals)
                        else:
                            apport = apportion_obj.browse(
                                cr, uid, apportionment_ids[0])
                            untaxed_amount = subtotal + apport.untaxed_amount
                            taxation_amount = cur_obj.round(
                                cr, uid, cur, (untaxed_amount * tax.amount))
                            total_amount = untaxed_amount + taxation_amount
                            apportion_obj.write(
                                cr, uid, [apport.id],
                                {'untaxed_amount': untaxed_amount,
                                 'taxation_amount': taxation_amount,
                                 'total_amount': total_amount})

        return True

    def write(self, cr, uid, ids, data, context=None):
        if context is None:
            context = {}

        data.update({'tax_apportionment_ids': [(6, 0, [])]})
        super(stock_picking, self).write(cr, uid, ids, data, context=context)
        self._calc_apportionment_taxes(cr, uid, ids, context=context)

        return True

    def refresh_tax_apportionment(self, cr, uid, ids, context=None):
        if context is None:
            context = {}

        self.write(cr, uid, ids,
                   {'tax_apportionment_ids': [(6, 0, [])]},
                   context=context)

        return True


class stock_move(orm.Model):

    _inherit = 'stock.move'

    def create(self, cr, uid, data, context=None):
        if context is None:
            context = {}

        move_id = super(stock_move, self).create(cr, uid,
                                                 data, context=context)

        if 'picking_id' in data:
            picking_obj = self.pool['stock.picking']
            picking_obj.write(cr, uid,
                              [data['picking_id']],
                              {'tax_apportionment_ids': [(6, 0, [])]})

        return move_id
