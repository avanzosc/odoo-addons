# Copyright 2021 Leire Martinez de Santos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api
from datetime import datetime


class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_current_year = fields.Boolean(compute='_compute_is_current_year',
                                     string="Is current year")
    is_current_month = fields.Boolean(compute='_compute_is_current_month',
                                      string="Is current month")

    @api.multi
    @api.depends('date_order')
    def _compute_is_current_year(self):
        today = datetime.today()
        for res in self:
            if res.date_order and\
                    today.year == res.date_order.year:
                res.is_current_year = True

    @api.multi
    @api.depends('date_order', 'is_current_year')
    def _compute_is_current_month(self):
        today = datetime.today()
        for res in self:
            if res.is_current_year and \
                    today.month == res.date_order.month:
                res.is_current_month = True
