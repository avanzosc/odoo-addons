# -*- coding: utf-8 -*-
# © 2016 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api


class ProcurementCustomStandarice(models.TransientModel):
    _name = 'procurement.custom.standarice'

    @api.multi
    def custom_qty_to_standard(self):
        for orderpoint in self.env['stock.warehouse.orderpoint'].browse(
                self._context.get('active_ids')):
            orderpoint.product_min_qty = orderpoint.custom_rule_min_qty
            orderpoint.product_max_qty = orderpoint.custom_rule_max_qty

    @api.multi
    def average_qty_to_rules(self):
        for orderpoint in self.env['stock.warehouse.orderpoint'].browse(
                self._context.get('active_ids')):
            orderpoint.product_min_qty = (
                orderpoint.company_id.stock_average_min_month *
                orderpoint.average_rule_qty)
            orderpoint.product_max_qty = (
                orderpoint.company_id.stock_average_max_month *
                orderpoint.average_rule_qty)
