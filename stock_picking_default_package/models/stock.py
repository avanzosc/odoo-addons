# Copyright 2021 Leire Martinez de Santos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    default_packaging_id = fields.Many2one(
        comodel_name='product.packaging', string='Default Packaging',
        related='product_id.categ_id.default_packaging_id')


class StockQuantPackage(models.Model):
    _inherit = 'stock.quant.package'

    expected_quantity = fields.Integer(
        string='Expected quantity', compute='_compute_expected_qty')
    quantity_in_package = fields.Integer(
        string='Quantity in package', compute='_compute_qty_in_package')

    def _compute_qty_in_package(self):
        for res in self:
            stock_move_line_ids = self.env['stock.move.line'].search([
                ('result_package_id.id', '=', res.id)])
            total_lines_qty = 0
            for line in stock_move_line_ids:
                total_lines_qty += line.qty_done
            res.quantity_in_package = total_lines_qty

    def _compute_expected_qty(self):
        for res in self:
            stock_move_line_ids = self.env['stock.move.line'].search([(
                'result_package_id.id', '=', res.id)])
            total_lines_qty = 0
            for line in stock_move_line_ids:
                total_lines_qty += line.product_uom_qty
            res.expected_quantity = total_lines_qty
