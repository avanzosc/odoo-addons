# -*- coding: utf-8 -*-
# © 2016 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models
from openerp.addons import decimal_precision as dp


class MrpProductionProductLine(models.Model):
    _inherit = 'mrp.production.product.line'

    @api.depends('subtotal', 'production_id.commercial_percent',
                 'production_id.profit_percent')
    def _compute_profit_commercial(self):
        for mrp in self:
            mrp.profit = \
                mrp.subtotal * (mrp.production_id.profit_percent / 100)
            mrp.commercial = \
                (mrp.subtotal + mrp.profit) * \
                (mrp.production_id.commercial_percent / 100)

    profit = fields.Float(
        string='Profit', compute='_compute_profit_commercial',
        digits=dp.get_precision('Product Price'))
    commercial = fields.Float(
        string='Commercial', compute='_compute_profit_commercial',
        digits=dp.get_precision('Product Price'))


class MrpProductionWorkcenterLine(models.Model):
    _inherit = 'mrp.production.workcenter.line'

    @api.depends('subtotal', 'production_id.commercial_percent',
                 'production_id.profit_percent')
    def _compute_profit_commercial(self):
        for mrp in self:
            mrp.profit = mrp.subtotal * \
                mrp.production_id.profit_percent / 100
            mrp.commercial = \
                (mrp.subtotal + mrp.profit) * \
                (mrp.production_id.commercial_percent / 100)

    profit = fields.Float(
        string='Profit', compute='_compute_profit_commercial',
        digits=dp.get_precision('Product Price'))
    commercial = fields.Float(
        string='Commercial', compute='_compute_profit_commercial',
        digits=dp.get_precision('Product Price'))


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    currency_id = fields.Many2one(
        comodel_name='res.currency', string='Currency',
        related='company_id.currency_id')
    profit_percent = fields.Float(string='Profit percentage')
    commercial_percent = fields.Float(string='Commercial percentage')
    external_commercial_percent = fields.Float(
        string='External commercial percentage')
    scheduled_profit = fields.Float(
        string='Profit', compute='_compute_scheduled_total',
        digits=dp.get_precision('Product Price'))
    scheduled_commercial = fields.Float(
        string='Commercial', compute='_compute_scheduled_total',
        digits=dp.get_precision('Product Price'))
    scheduled_cost_total = fields.Float(
        string='Scheduled Total', compute='_compute_scheduled_total',
        digits=dp.get_precision('Product Price'))
    routing_profit = fields.Float(
        string='Profit', compute='_compute_routing_total',
        digits=dp.get_precision('Product Price'))
    routing_commercial = fields.Float(
        string='Commercial', compute='_compute_routing_total',
        digits=dp.get_precision('Product Price'))
    routing_cost_total = fields.Float(
        string='Routing Total', compute='_compute_routing_total',
        digits=dp.get_precision('Product Price'))
    commercial_total = fields.Float(
        string='Commercial', compute='_compute_commercial',
        digits=dp.get_precision('Product Price'))
    external_commercial_total = fields.Float(
        string='External Commercial', compute='_compute_commercial',
        digits=dp.get_precision('Product Price'))
    external_total = fields.Float(
        string='External Total', compute='_compute_commercial',
        digits=dp.get_precision('Product Price'))
    production_total_unit = fields.Float(
        string='Total (by unit)', compute="_compute_production_total",
        digits=dp.get_precision('Product Price'))

    @api.depends('profit_percent', 'commercial_percent',
                 'product_lines', 'product_lines.subtotal')
    def _compute_scheduled_total(self):
        for prod in self.filtered(lambda m: m.product_lines and
                                  m.product_qty):
            super(MrpProduction, prod)._compute_scheduled_total()
            prod.scheduled_profit =\
                prod.scheduled_total * (prod.profit_percent / 100)
            prod.scheduled_cost_total =\
                prod.scheduled_total * ((100 + prod.profit_percent) / 100)
            prod.scheduled_commercial =\
                prod.scheduled_cost_total * (prod.commercial_percent / 100)

    @api.depends('profit_percent', 'commercial_percent',
                 'workcenter_lines', 'workcenter_lines.subtotal')
    def _compute_routing_total(self):
        for prod in self.filtered(lambda m: m.workcenter_lines and
                                  m.product_qty):
            super(MrpProduction, prod)._compute_routing_total()
            prod.routing_profit =\
                prod.routing_total * (prod.profit_percent / 100)
            prod.routing_cost_total =\
                prod.routing_total * ((100 + prod.profit_percent) / 100)
            prod.routing_commercial =\
                prod.routing_cost_total * (prod.commercial_percent / 100)

    @api.depends('production_total', 'commercial_percent',
                 'external_commercial_percent')
    def _compute_commercial(self):
        for prod in self:
            prod.commercial_total =\
                prod.production_total * (prod.commercial_percent / 100)
            prod.external_commercial_total = prod.production_total *\
                (prod.external_commercial_percent / 100)
            prod.external_total = prod.production_total *\
                ((100 + prod.external_commercial_percent) / 100)

    @api.depends('product_qty', 'scheduled_cost_total', 'routing_cost_total')
    def _compute_production_total(self):
        by_unit = self.env['mrp.config.settings']._get_parameter(
            'subtotal.by.unit')
        for prod in self:
            super(MrpProduction, prod)._compute_production_total()
            total = prod.routing_cost_total + prod.scheduled_cost_total
            prod.production_total =\
                total * (prod.product_qty if by_unit else 1)
            prod.production_total_unit =\
                prod.production_total / (prod.product_qty or 1.0)
