# -*- coding: utf-8 -*-
# © 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import _, api, models, fields


class StockInventoryLine(models.Model):
    _inherit = 'stock.inventory.line'

    @api.multi
    @api.depends('standard_price', 'product_qty')
    def _compute_value(self):
        for line in self:
            line.value = line.product_qty * line.standard_price

    @api.multi
    @api.depends('product_id')
    def _compute_under_repair(self):
        repair_line = self.env['mrp.repair.line']
        for line in self:
            line.under_repair = len(repair_line.search([
                '&', ('product_id', '=', line.product_id.id),
                ('state', '=', 'confirmed')]))

    @api.multi
    @api.depends('theoretical_qty', 'under_repair')
    def _compute_net_qty(self):
        for line in self:
            line.net_qty = line.theoretical_qty - line.under_repair

    @api.multi
    @api.depends('net_qty', 'standard_price')
    def _compute_net_value(self):
        for line in self:
            line.net_value = line.net_qty * line.standard_price

    standard_price = fields.Float(related='product_id.standard_price')
    value = fields.Float(compute='_compute_value')
    under_repair = fields.Integer(compute='_compute_under_repair')
    net_qty = fields.Float(compute='_compute_net_qty')
    net_value = fields.Float(compute='_compute_net_value')
