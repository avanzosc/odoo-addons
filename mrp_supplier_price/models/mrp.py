# -*- coding: utf-8 -*-
# © 2016 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api
from openerp.addons import decimal_precision as dp


class MrpProductionProductLine(models.Model):
    _inherit = 'mrp.production.product.line'

    @api.depends('product_id.uop_coeff', 'product_qty')
    def _compute_uop_qty(self):
        for line in self.filtered('product_id'):
            line.uop_qty = line.product_qty * line.product_id.uop_coeff

    @api.depends('cost', 'product_id.uop_coeff')
    def _compute_uop_price(self):
        for line in self.filtered('product_id'):
            line.uop_price = line.cost / (line.product_id.uop_coeff or 1.0)

    @api.depends('product_id.uop_id', 'product_id.uom_po_id')
    def _compute_product_uop(self):
        for line in self.filtered('product_id'):
            line.uop_id = line.product_id.uop_id or line.product_id.uom_po_id

    @api.depends('product_id.seller_ids')
    def _compute_variant_suppliers(self):
        for line in self.filtered('product_id'):
            line.supplier_id_domain = line.product_id.seller_ids.mapped('name')

    supplier_id = fields.Many2one(
        comodel_name='res.partner', string='Supplier')
    supplier_id_domain = fields.Many2many(
        comodel_name='res.partner', compute='_compute_variant_suppliers')
    cost = fields.Float(
        string='Cost', digits=dp.get_precision('Product Price'))
    unit_final_cost = fields.Float(
        string='Final Unit Cost', compute='_compute_subtotal',
        digits=dp.get_precision('Product Price'),
        help='Cost by final product unit.')
    subtotal = fields.Float(
        string='Subtotal', compute='_compute_subtotal',
        digits=dp.get_precision('Product Price'))
    uop_id = fields.Many2one(
        string='Product UoP', comodel_name='product.uom',
        compute='_compute_product_uop')
    uop_qty = fields.Float(
        string='Product UoP Quantity', compute='_compute_uop_qty',
        digits=dp.get_precision('Product Unit of Measure'))
    uop_price = fields.Float(
        string='Purchase Price', compute='_compute_uop_price',
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

    @api.depends('cost', 'product_qty', 'production_id',
                 'production_id.product_qty')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.product_qty * line.cost
            line.unit_final_cost = (
                line.subtotal / (line.production_id.product_qty or 1.0))

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

    profit_percent = fields.Float(string='Profit percentage')
    commercial_percent = fields.Float(string='Commercial percentage')
    scheduled_total = fields.Float(
        string='Total', compute='_compute_scheduled_total',
        digits=dp.get_precision('Product Price'))
    production_total = fields.Float(
        string='Production Total', compute='_compute_production_total',
        digits=dp.get_precision('Product Price'))

    @api.depends('product_lines', 'product_lines.subtotal')
    def _compute_scheduled_total(self):
        by_unit = self.env['mrp.config.settings']._get_parameter(
            'subtotal.by.unit')
        for mrp in self.filtered(lambda m: m.product_lines and m.product_qty):
            subtotal = sum(mrp.mapped('product_lines.subtotal'))
            mrp.scheduled_total =\
                subtotal / mrp.product_qty if by_unit else subtotal

    @api.depends('scheduled_total')
    def _compute_production_total(self):
        by_unit = self.env['mrp.config.settings']._get_parameter(
            'subtotal.by.unit')
        for prod in self:
            total = prod.scheduled_total
            try:
                total += prod.routing_total
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

    @api.multi
    def action_compute(self, properties=None):
        res = super(MrpProduction, self).action_compute(properties=properties)
        for line in self.product_lines:
            line.onchange_product_product_qty()
        return res
