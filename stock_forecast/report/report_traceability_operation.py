# -*- coding: utf-8 -*-
# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api
from openerp.addons import decimal_precision as dp


class ReportStockTraceabilityOperation(models.TransientModel):
    _inherit = 'report.stock.traceability_operation'

    available_qty = fields.Float(
        string='Available qty',
        digits_compute=dp.get_precision('Product Unit of Measure'))
    virtual_available = fields.Float(
        string='Available virtual',
        digits_compute=dp.get_precision('Product Unit of Measure'))
    incoming_qty = fields.Float(
        string='Incoming Amount Pending',
        digits_compute=dp.get_precision('Product Unit of Measure'))
    outgoing_qty = fields.Float(
        string='Outgoing Amount Pending',
        digits_compute=dp.get_precision('Product Unit of Measure'))

    @api.model
    def create(self, values):
        names = ['qty_available', 'virtual_available',
                 'incoming_qty', 'outgoing_qty']
        if (values.get('date_expected', False) and
                values.get('product_id', False)):
            product = self.env['product.product'].browse(
                values.get('product_id'))
            date_expected = fields.Datetime.from_string(
                values.get('date_expected')).date()
            res = product.with_context(
                to_date_expected=fields.Datetime.to_string(
                    date_expected))._product_available(field_names=names)
            if res:
                values.update(
                    {'available_qty': res.get(product.id).get('qty_available'),
                     'virtual_available':
                     res.get(product.id).get('virtual_available'),
                     'incoming_qty': res.get(product.id).get('incoming_qty'),
                     'outgoing_qty': res.get(product.id).get('outgoing_qty')})
        return super(ReportStockTraceabilityOperation, self).create(values)
