# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp.osv import orm
from openerp.tools import float_compare, float_round
from psycopg2 import OperationalError
import openerp


class ProcurementOrder(orm.Model):
    _inherit = 'procurement.order'

    def _procure_orderpoint_confirm(self, cr, uid, use_new_cursor=False,
                                    company_id=False, context=None):
        orderpoint_obj = self.pool['stock.warehouse.orderpoint']
        if use_new_cursor:
            cr = openerp.registry(cr.dbname).cursor()
        cond = company_id and [('company_id', '=', company_id)] or []
        cond = self._prepare_orderpoint_search_condition(
            cr, uid, cond, context=context)
        orderpoints_ids = orderpoint_obj.search(cr, uid, cond, context=context)
        orderpoints = orderpoint_obj.browse(
            cr, uid, orderpoints_ids, context=context)
        if context.get('categories_filter', False):
            orderpoint_ids = orderpoints.filtered(
                lambda x: x.product_id.categ_id.id in
                context.get('categories_filter').ids).ids
        else:
            orderpoint_ids = orderpoints.ids
        prev_ids = []
        while orderpoint_ids:
            ids = orderpoint_ids[:100]
            del orderpoint_ids[:100]
            for op in orderpoint_obj.browse(cr, uid, ids, context=context):
                try:
                    prods = self._product_virtual_get(cr, uid, op)
                    if prods is None:
                        continue
                    self._make_calculations_for_create_procurement(
                        cr, uid, prods, op, use_new_cursor, context=context)
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

    def _make_calculations_for_create_procurement(
            self, cr, uid, prods, op, use_new_cursor, context=None):
        procurement_obj = self.pool['procurement.order']
        orderpoint_obj = self.pool['stock.warehouse.orderpoint']
        result = float_compare(prods, op.product_min_qty,
                               precision_rounding=op.product_uom.rounding)
        if result < 0:
            qty = (max(op.product_min_qty, op.product_max_qty) - prods)
            reste = (op.qty_multiple > 0 and qty % op.qty_multiple or 0.0)
            result = float_compare(reste, 0.0,
                                   precision_rounding=op.product_uom.rounding)
            if result > 0:
                qty += op.qty_multiple - reste
            result = float_compare(qty, 0.0,
                                   precision_rounding=op.product_uom.rounding)
            if result > 0:
                qty -= orderpoint_obj.subtract_procurements(
                    cr, uid, op, context=context)
                qty_rounded = float_round(
                    qty, precision_rounding=op.product_uom.rounding)
                if qty_rounded > 0:
                    vals = self._prepare_orderpoint_procurement(
                        cr, uid, op, qty_rounded, context=context)
                    proc_id = procurement_obj.create(
                        cr, uid, vals, context=context)
                    self.check(cr, uid, [proc_id])
                    self.run(cr, uid, [proc_id])
        if use_new_cursor:
            cr.commit()

    def _prepare_orderpoint_search_condition(self, cr, uid, cond,
                                             context=None):
        if context.get('locations_filter', False):
            cond.append(('location_id', 'in',
                         context.get('locations_filter').ids))
        return cond
