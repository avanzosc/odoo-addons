# -*- coding: utf-8 -*-
# © 2016 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models
from openerp.addons import decimal_precision as dp


class MrpProductionWorkcenterLine(models.Model):
    _inherit = 'mrp.production.workcenter.line'

    costs_hour = fields.Float(
        string='Cost per hour', digits=dp.get_precision('Product Price'))
    costs_cycle = fields.Float(
        string='Cost per cycle', digits=dp.get_precision('Product Price'))
    op_number = fields.Integer(string='Operators')
    op_avg_cost = fields.Float(
        string='Operators avg. cost', digits=dp.get_precision('Product Price'))
    subtotal_hour = fields.Float(
        string='Subtotal by hours', compute='_compute_subtotals',
        digits=dp.get_precision('Product Price'))
    subtotal_operator = fields.Float(
        string='Subtotal by operators', compute='_compute_subtotals',
        digits=dp.get_precision('Product Price'))
    subtotal_cycle = fields.Float(
        string='Subtotal by cycle', compute='_compute_subtotals',
        digits=dp.get_precision('Product Price'))
    subtotal = fields.Float(
        string='Subtotal', compute='_compute_subtotals',
        digits=dp.get_precision('Product Price'))
    unit_final_cost = fields.Float(
        string='Final Unit Cost', compute='_compute_subtotals',
        digits=dp.get_precision('Product Price'),
        help='Cost by final product unit.')

    @api.depends('workcenter_id', 'workcenter_id.costs_hour',
                 'workcenter_id.costs_cycle', 'workcenter_id.op_number',
                 'workcenter_id.op_avg_cost', 'workcenter_id.fixed_hour_cost',
                 'workcenter_id.fixed_cycle_cost')
    def _compute_subtotals(self):
        for line in self:
            line.subtotal_hour = line.hour * line.costs_hour
            line.subtotal_cycle = line.cycle * line.costs_cycle
            line.subtotal_operator = \
                line.hour * line.op_avg_cost * line.op_number
            line.subtotal =\
                line.subtotal_hour + line.subtotal_cycle +\
                line.subtotal_operator
            line.unit_final_cost = \
                line.subtotal / (line.production_id.product_qty or 1.0)

    @api.onchange('workcenter_id')
    def onchange_workcenter_id(self):
        for line in self.filtered('workcenter_id'):
            line.costs_hour = line.workcenter_id.costs_hour
            line.costs_cycle = line.workcenter_id.costs_cycle
            line.op_number = line.workcenter_id.op_number
            line.op_avg_cost = line.workcenter_id.op_avg_cost


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    routing_cycle_total = fields.Float(
        string='Total (Cycle)', compute='_compute_routing_total',
        digits=dp.get_precision('Product Price'))
    routing_hour_total = fields.Float(
        string='Total (Hour)', compute='_compute_routing_total',
        digits=dp.get_precision('Product Price'))
    routing_total = fields.Float(
        string='Total', compute='_compute_routing_total',
        digits=dp.get_precision('Product Price'))
    routing_operator_total = fields.Float(
        string='Total (Operator)', compute='_compute_routing_total',
        digits=dp.get_precision('Product Price'))
    production_total = fields.Float(
        string='Production Total', compute='_compute_production_total',
        digits=dp.get_precision('Product Price'))

    @api.depends('workcenter_lines', 'workcenter_lines.subtotal')
    def _compute_routing_total(self):
        by_unit = self.env['mrp.config.settings']._get_parameter(
            'subtotal.by.unit')
        for mrp in self.filtered(lambda m: m.workcenter_lines and
                                 m.product_qty):
            subtotal = sum(
                mrp.mapped('workcenter_lines.subtotal_cycle'))
            mrp.routing_cycle_total =\
                subtotal / mrp.product_qty if by_unit else subtotal
            subtotal = sum(
                mrp.mapped('workcenter_lines.subtotal_hour'))
            mrp.routing_hour_total =\
                subtotal / mrp.product_qty if by_unit else subtotal
            subtotal = sum(
                mrp.mapped('workcenter_lines.subtotal_operator'))
            mrp.routing_operator_total =\
                subtotal / mrp.product_qty if by_unit else subtotal
            mrp.routing_total =\
                mrp.routing_cycle_total + mrp.routing_hour_total + \
                mrp.routing_operator_total

    @api.multi
    def _compute_production_total(self):
        by_unit = self.env['mrp.config.settings']._get_parameter(
            'subtotal.by.unit')
        for prod in self:
            total = prod.routing_total
            try:
                total += prod.scheduled_total
            except:
                pass
            prod.production_total =\
                total * (prod.product_qty if by_unit else 1)

    @api.multi
    def button_recompute_total(self):
        fields_list = ['production_total']
        for field in fields_list:
            self.env.add_todo(self._fields[field], self)
        self.recompute()


class MrpWorkcenter(models.Model):
    _inherit = 'mrp.workcenter'

    fixed_hour_cost = fields.Boolean(string='Fixed hour cost', default=False)
    fixed_cycle_cost = fields.Boolean(string='Fixed cycle cost', default=False)


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    @api.multi
    def _prepare_wc_line(self, wc_use, level=0, factor=1):
        self.ensure_one()
        vals = super(MrpBom, self)._prepare_wc_line(
            wc_use, level=level, factor=factor)
        workcenter = self.env['mrp.workcenter'].browse(
            vals.get('workcenter_id'))
        vals.update({
            'cycle': workcenter.capacity_per_cycle
            if workcenter.fixed_cycle_cost else vals.get('cycle'),
            'hour': workcenter.time_cycle if workcenter.fixed_hour_cost
            else vals.get('hour'),
            'costs_hour': workcenter.costs_hour,
            'costs_cycle': workcenter.costs_cycle,
            'op_number': workcenter.op_number,
            'op_avg_cost': workcenter.op_avg_cost,
        })
        return vals
