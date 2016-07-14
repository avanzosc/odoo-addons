# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api
import openerp.addons.decimal_precision as dp
from dateutil.relativedelta import relativedelta
from openerp.tools import float_compare, float_round
from psycopg2 import OperationalError
import openerp


class StockWarehouseOrderpoint(models.Model):
    _inherit = 'stock.warehouse.orderpoint'

    @api.multi
    def _get_custom_rule(self):
        for orderpoint in self:
            if orderpoint.custom_stock_planning_rule:
                self._calculate_custom_rule(orderpoint)

    def _calculate_custom_rule(self, orderpoint):
        move_obj = self.env['stock.move']
        min = orderpoint.company_id.stock_planning_min_days
        min = min * -1
        max = orderpoint.company_id.stock_planning_max_days
        max = max * -1
        fdate = fields.Date.to_string(
            fields.Date.from_string(fields.Date.context_today(self)) +
            relativedelta(days=min))
        moves = move_obj._find_moves_from_stock_planning(
            orderpoint.company_id, fields.Date.context_today(self),
            from_date=fdate,
            product=orderpoint.product_id, location_id=orderpoint.location_id)
        orderpoint.custom_rule_min_qty = sum(
            moves.mapped('product_uom_qty'))
        fdate = fields.Date.to_string(
            fields.Date.from_string(fields.Date.context_today(self)) +
            relativedelta(days=max))
        moves = move_obj._find_moves_from_stock_planning(
            orderpoint.company_id, fields.Date.context_today(self),
            from_date=fdate,
            product=orderpoint.product_id, location_id=orderpoint.location_id)
        orderpoint.custom_rule_max_qty = sum(
            moves.mapped('product_uom_qty'))

    @api.multi
    def custom_qty_to_standar(self):
        for orderpoint in self.search([]):
            orderpoint.product_min_qty = orderpoint.custom_rule_min_qty
            orderpoint.product_max_qty = orderpoint.custom_rule_max_qty

    custom_stock_planning_rule = fields.Boolean(
        string='customize min. qty, and max. qty rules',
        related='company_id.custom_stock_planning_rule')
    custom_rule_min_qty = fields.Float(
        'Custom rule min. qty', compute='_get_custom_rule',
        digits_compute=dp.get_precision('Product Unit of Measure'))
    custom_rule_max_qty = fields.Float(
        'Custom rule max. qty', compute='_get_custom_rule',
        digits_compute=dp.get_precision('Product Unit of Measure'))


class ProcurementOrder(models.Model):
    _inherit = "procurement.order"

    def _procure_orderpoint_confirm(
            self, cr, uid, use_new_cursor=False,
            company_id=False, context=None):
        '''
        Create procurement based on Orderpoint

        :param bool use_new_cursor: if set, use a dedicated cursor and
        auto-commit after processing each procurement.
            This is appropriate for batch jobs only.
        '''
        if context is None:
            context = {}
        if use_new_cursor:
            cr = openerp.registry(cr.dbname).cursor()
        orderpoint_obj = self.pool.get('stock.warehouse.orderpoint')

        procurement_obj = self.pool.get('procurement.order')
        dom = company_id and [('company_id', '=', company_id)] or []
        if context.get('orderpoints_ids'):
            dom.append(('id', 'in', context.get('orderpoints_ids')))
        else:
            return super(ProcurementOrder, super)._procure_orderpoint_confirm(
                cr, uid, use_new_cursor=use_new_cursor,
                company_id=company_id, context=context
            )
        orderpoint_ids = orderpoint_obj.search(cr, uid, dom)
        prev_ids = []
        while orderpoint_ids:
            ids = orderpoint_ids[:100]
            del orderpoint_ids[:100]
            for op in orderpoint_obj.browse(cr, uid, ids, context=context):
                try:
                    prods = self._product_virtual_get(cr, uid, op)
                    if prods is None:
                        continue
                    if float_compare(
                            prods, op.product_min_qty,
                            precision_rounding=op.product_uom.rounding) < 0:
                        qty = max(
                            op.product_min_qty, op.product_max_qty) - prods
                        reste = op.qty_multiple > 0 and qty % \
                            op.qty_multiple or 0.0
                        if float_compare(
                                reste, 0.0,
                                precision_rounding=op.product_uom.rounding)\
                                > 0:
                            qty += op.qty_multiple - reste

                        if float_compare(
                                qty, 0.0,
                                precision_rounding=op.product_uom.rounding)\
                                <= 0:
                            continue

                        qty -= orderpoint_obj.subtract_procurements(
                            cr, uid, op, context=context)

                        qty_rounded = float_round(
                            qty, precision_rounding=op.product_uom.rounding)
                        if qty_rounded > 0:
                            proc_id = procurement_obj.create(
                                cr, uid,
                                self._prepare_orderpoint_procurement(
                                    cr, uid, op, qty_rounded,
                                    context=context), context=context)
                            self.check(cr, uid, [proc_id])
                            self.run(cr, uid, [proc_id])
                    if use_new_cursor:
                        cr.commit()
                except OperationalError:
                    if use_new_cursor:
                        orderpoint_ids.append(op.id)
                        cr.rollback()
                        continue
                    else:
                        raise
            if use_new_cursor:
                cr.commit()
            if prev_ids == ids:
                break
            else:
                prev_ids = ids

        if use_new_cursor:
            cr.commit()
            cr.close()
        return {}
