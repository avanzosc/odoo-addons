# -*- coding: utf-8 -*-
# © 2016 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api


class MrpProductionProductLine(models.Model):

    _inherit = 'mrp.production.product.line'

    supplier_id = fields.Many2one(comodel_name='res.partner')
    cost = fields.Float(string='Cost')
    subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal')

    def _select_best_supplier(self):
        best_price={}
        for line in self.product_id.supplier_ids:
            for price_line in line.pricelist_ids:
                if price_line.min_quantity >= self.product_qty:
                    best_price = {'supplier_id': line.name,
                                  'cost': price_line.price}
        return best_price

    @api.depends('cost', 'product_qty')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.product_qty * line.cost

    @api.onchange('product_id', 'product_qty')
    def onchange_supplier_id(self):
        for line in self:
            best_supplier = line._select_best_supplier()
            if best_supplier:
                line.supplier_id = best_supplier['supplier_id']
                line.cost = best_supplier['cost']


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    @api.depends('product_lines')
    def _schedule_total(self):
        for mrp in self:
            subtotal = mrp.product_lines.mapped('subtotal')
            mrp.scheduled_total = subtotal and sum(subtotal) or 0

    @api.depends('profit_percent', 'scheduled_total')
    def _compute_profit(self):
        for mrp in self:
            mrp.profit = mrp.scheduled_total * mrp.profit_percent
            mrp.commercial = (mrp.scheduled_total + mrp.profit) * mrp.commercial_percent

    scheduled_total = fields.Float(string='Scheduled Total',
                                   compute='_schedule_total')
    profit = fields.Float(string='Profit',
                          compute='_compute_profit')
    profit_percent = fields.Float(string='Profit per')
    commercial = fields.Float(string='Commercial',
                          compute='_compute_profit')
    commercial_percent = fields.Float(string='Commercial per')