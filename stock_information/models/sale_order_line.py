# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api
from dateutil.relativedelta import relativedelta


class saleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    @api.multi
    @api.depends('order_id', 'order_id.date_order', 'delay')
    def _compute_date_planned(self):
        for line in self:
            new_date = fields.Date.context_today(self)
            if line.order_id and line.order_id.date_order:
                new_date = fields.Datetime.from_string(
                    line.order_id.date_order).date()
                if line.delay:
                    new_date = (new_date +
                                (relativedelta(days=line.delay)))
            line.date_planned = new_date

    date_planned = fields.Date(
        'Date planned', compute='_compute_date_planned', store=True,
        default=_compute_date_planned)

    def _find_sale_lines_from_stock_information(
            self, company, to_date, product, location, from_date=None):
        cond = [('company_id', '=', company.id),
                ('product_id', '=', product.id),
                ('date_planned', '<=', to_date),
                ('state', '=', 'draft')]
        if from_date:
            cond.append(('date_planned', '>=', from_date))
        sale_lines = self.search(cond)
        sale_lines = sale_lines.filtered(
            lambda x: x.order_id.state not in ('cancel', 'except_picking',
                                               'except_invoice', 'done',
                                               'approved'))
        sale_lines = sale_lines.filtered(
            lambda x: x.order_id.warehouse_id.lot_stock_id.id == location.id)
        return sale_lines
