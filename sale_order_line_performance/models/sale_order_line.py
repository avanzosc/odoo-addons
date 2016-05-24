# -*- coding: utf-8 -*-
# © 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.model
    def _calc_line_quantity(self, line):
        qty = super(SaleOrderLine, self)._calc_line_quantity(line)
        if line.performance and line.apply_performance:
            qty = qty * line.performance
        return qty

    performance = fields.Float(
        'Performance', help='Estimated time for completion the task')
    apply_performance = fields.Boolean(
        string='Applied performance to calculating the price', default=True)

    @api.multi
    def product_id_change(
            self, pricelist, product, qty=0, uom=False, qty_uos=0, uos=False,
            name='', partner_id=False, lang=False, update_tax=True,
            date_order=False, packaging=False, fiscal_position=False,
            flag=False):
        res = super(SaleOrderLine, self). product_id_change(
            pricelist, product, qty=qty, uom=uom, qty_uos=qty_uos,
            uos=uos, name=name, partner_id=partner_id, lang=lang,
            update_tax=update_tax, date_order=date_order, packaging=packaging,
            fiscal_position=fiscal_position, flag=flag)
        if product:
            p = self.env['product.product'].browse(product)
            res['value']['performance'] = p.performance
        return res
