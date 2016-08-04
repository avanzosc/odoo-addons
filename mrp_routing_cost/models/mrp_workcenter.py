# -*- coding: utf-8 -*-
# © 2016 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class MrpProductionWorkcenterLine(models.Model):
    _inherit = 'mrp.production.workcenter.line'

    workcenter_costs_hour = fields.Float(
        string='Cost per hour', related='workcenter_id.costs_hour')
    workcenter_costs_cycle = fields.Float(
        string='Cost per cycle', related='workcenter_id.costs_cycle')
    workcenter_subtotal_hour = fields.Float(
        string='Subtotal by hours', compute='_compute_subtotals')
    workcenter_subtotal_cycle = fields.Float(
        string='Subtotal by cycle', compute='_compute_subtotals')
    workcenter_subtotal = fields.Float(
        string='Subtotal', compute='_compute_subtotals')

    @api.depends('workcenter_id', 'workcenter_id.costs_hour',
                 'workcenter_id.costs_cycle')
    def _compute_subtotals(self):
        for line in self:
            line.workcenter_subtotal_hour =\
                line.hour * line.workcenter_id.costs_hour
            line.workcenter_subtotal_cycle =\
                line.cycle * line.workcenter_id.costs_cycle
            line.workcenter_subtotal =\
                line.workcenter_subtotal_hour + line.workcenter_subtotal_cycle


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    routing_cycle_total = fields.Float(
        string='Total (Cycle)', compute='_compute_routing_total')
    routing_hour_total = fields.Float(
        string='Total (Hour)', compute='_compute_routing_total')
    routing_total = fields.Float(
        string='Total', compute='_compute_routing_total')
    production_total = fields.Float(
        string='Production Total', compute='_compute_production_total')

    @api.depends('workcenter_lines',
                 'workcenter_lines.workcenter_subtotal_hour',
                 'workcenter_lines.workcenter_subtotal_cycle')
    def _compute_routing_total(self):
        for prod in self:
            prod.routing_cycle_total = \
                sum(prod.mapped('workcenter_lines.workcenter_subtotal_cycle'))
            prod.routing_hour_total =\
                sum(prod.mapped('workcenter_lines.workcenter_subtotal_hour'))
            prod.routing_total =\
                prod.routing_cycle_total + prod.routing_hour_total

    @api.multi
    def _compute_production_total(self):
        for prod in self:
            total = prod.routing_total
            try:
                total += prod.cost_total
            except:
                pass
            prod.production_total = total
