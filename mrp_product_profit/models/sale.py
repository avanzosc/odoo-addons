# -*- coding: utf-8 -*-
# © 2016 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    scheduled_total = fields.Float(related='mrp_production_id.scheduled_total')
    scheduled_profit = fields.Float(
        related='mrp_production_id.scheduled_profit')
    profit_percent = fields.Float(related='mrp_production_id.profit_percent')
    scheduled_commercial = fields.Float(
        related='mrp_production_id.scheduled_commercial')
    commercial_percent = fields.Float(
        related='mrp_production_id.commercial_percent')
    scheduled_cost_total = fields.Float(
        related='mrp_production_id.scheduled_cost_total')

    @api.multi
    def button_recompute_total(self):
        for line in self.product_line_ids:
            line._compute_profit_commercial()
