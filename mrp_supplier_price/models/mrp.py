# -*- coding: utf-8 -*-
# © 2016 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api
from openerp.addons import decimal_precision as dp


class MrpProductionProductLine(models.Model):
    _inherit = 'mrp.production.product.line'

    supplier_id = fields.Many2one(
        comodel_name='res.partner', string='Supplier')
    cost = fields.Float(
        string='Cost', digits=dp.get_precision('Product Price'))
    subtotal = fields.Float(
        string='Subtotal', compute='_compute_subtotal',
        digits=dp.get_precision('Product Price'))

    def _select_best_cost_price(self, supplier_id=None):
        best_price = {}
        if supplier_id:
            supplier_ids = self.product_id.seller_ids.filtered(
                lambda x: x.name == supplier_id)
        else:
            supplier_ids = self.product_id.seller_ids
        for line in supplier_ids.mapped('pricelist_ids').filtered(
                lambda l: l.min_quantity <= self.product_qty):
            if not best_price or line.min_quantity <= \
                    self.product_qty and \
                    best_price['cost'] > line.price:
                best_price = {'supplier_id': line.suppinfo_id.name,
                              'cost': line.price}
        return best_price

    @api.depends('cost', 'product_qty')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.product_qty * line.cost

    @api.onchange('product_tmpl_id', 'product_id', 'product_qty')
    def onchange_product_product_qty(self):
        for line in self:
            best_supplier = line._select_best_cost_price()
            if best_supplier:
                line.supplier_id = best_supplier['supplier_id']
                line.cost = best_supplier['cost']
            else:
                line.cost = line.product_id.standard_price

    @api.onchange('supplier_id')
    def onchange_supplier_id(self):
        for line in self:
            best_price = line._select_best_cost_price(
                supplier_id=line.supplier_id)
            if best_price:
                line.supplier_id = best_price['supplier_id']
                line.cost = best_price['cost']


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    scheduled_total = fields.Float(
        string='Scheduled Total', compute='_compute_scheduled_total',
        digits=dp.get_precision('Product Price'))
    profit_percent = fields.Float(string='Profit percentage')
    commercial_percent = fields.Float(string='Commercial percentage')
    profit = fields.Float(
        string='Profit', compute='_compute_cost_total',
        digits=dp.get_precision('Product Price'))
    commercial = fields.Float(
        string='Commercial', compute='_compute_cost_total',
        digits=dp.get_precision('Product Price'))
    cost_total = fields.Float(
        string='Total', compute='_compute_cost_total',
        digits=dp.get_precision('Product Price'))
    production_total = fields.Float(
        string='Production Total', compute='_compute_production_total')

    @api.depends('product_lines', 'product_lines.subtotal')
    def _compute_scheduled_total(self):
        for mrp in self:
            subtotal = mrp.mapped('product_lines.subtotal')
            mrp.scheduled_total = subtotal and sum(subtotal) or 0

    @api.depends('profit_percent', 'scheduled_total', 'commercial_percent')
    def _compute_cost_total(self):
        for mrp in self:
            mrp.profit = mrp.scheduled_total * (mrp.profit_percent / 100)
            mrp.cost_total =\
                mrp.scheduled_total * ((100 + mrp.profit_percent) / 100)
            mrp.commercial =\
                mrp.cost_total * (mrp.commercial_percent / 100)

    @api.depends('cost_total')
    def _compute_production_total(self):
        for prod in self:
            total = prod.cost_total
            try:
                total += prod.routing_total
            except:
                pass
            prod.production_total = total

    @api.multi
    def button_recompute_total(self):
        fields_list = ['production_total']
        for field in fields_list:
            self.env.add_todo(self._fields[field], self)
        self.recompute()
