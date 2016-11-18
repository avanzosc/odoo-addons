# -*- coding: utf-8 -*-
# © 2016 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class MrpProductionProductLine(models.Model):
    _inherit = 'mrp.production.product.line'

    @api.multi
    @api.depends('production_id.commercial_percent', 'subtotal',
                 'production_id.profit_percent')
    def _compute_profit_commercial(self):
        for mrp in self:
            mrp.profit = \
                mrp.subtotal * (mrp.production_id.profit_percent / 100)
            mrp.commercial = \
                (mrp.subtotal + mrp.profit) * \
                (mrp.production_id.commercial_percent / 100)

    profit = fields.Float(
        string='Profit', compute='_compute_profit_commercial')
    commercial = fields.Float(
        string='Commercial', compute='_compute_profit_commercial')


class MrpProductionWorkcenterLine(models.Model):
    _inherit = 'mrp.production.workcenter.line'

    @api.multi
    @api.depends('subtotal', 'production_id.profit_percent',
                 'production_id.commercial_percent')
    def _compute_profit_commercial(self):
        for mrp in self:
            mrp.profit = mrp.subtotal * \
                mrp.production_id.profit_percent / 100
            mrp.commercial = \
                (mrp.subtotal + mrp.profit) * \
                (mrp.production_id.commercial_percent / 100)

    profit = fields.Float(
        string='Profit', compute='_compute_profit_commercial')
    commercial = fields.Float(
        string='Commercial', compute='_compute_profit_commercial')


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    @api.depends('workcenter_lines',
                 'workcenter_lines.profit',
                 'workcenter_lines.subtotal_hour',
                 'workcenter_lines.subtotal_cycle')
    def _compute_routing_total(self):
        for prod in self:
            prod.routing_cycle_total = \
                sum(prod.mapped('workcenter_lines.subtotal_cycle'))
            prod.routing_hour_total =\
                sum(prod.mapped('workcenter_lines.subtotal_hour'))
            prod.routing_operator_total =\
                sum(prod.mapped('workcenter_lines.subtotal_operator'))
            prod.routing_profit = sum(prod.mapped('workcenter_lines.profit'))
            prod.routing_total =\
                prod.routing_cycle_total + prod.routing_hour_total + \
                prod.routing_operator_total + prod.routing_profit

    routing_profit = fields.Float(
        string='Total (Profit)', compute='_compute_routing_total')
