# -*- coding: utf-8 -*-
# © 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class StockPrintLabelLine(models.TransientModel):

    _name = "stock.print.label.line"

    wiz_id = fields.Many2one(comodel_name='stock.print.label',
                             string='Wizard')
    product_id = fields.Many2one(comodel_name='product.product',
                                 string='Product')
    lot_id = fields.Many2one(comodel_name='stock.production.lot', string='Lot')
    quant_id = fields.Many2one(comodel_name='stock.quant', string='Quant')
    quant_qty = fields.Float(string="Qty")
    package_qty = fields.Integer(string='Package Qty')
    ul_id = fields.Many2one(comodel_name='product.ul', string='Packaging')

    @api.multi
    @api.onchange('ul_id')
    def onchange_package_id(self):
        self.ensure_one()
        self.package_qty = self.quant_qty / (self.ul_id.qty or 1)


class StockPrintLabel(models.TransientModel):
    _name = "stock.print.label"

    @api.multi
    def _default_lines(self):
        active_model = self.env.context.get('active_model')
        active_model_obj = self.env[active_model]
        record = active_model_obj.browse(self.env.context.get('active_id'))
        moves = self.env['stock.move']
        if active_model == 'stock.picking':
            moves = record.move_lines.filtered(lambda x: x.state == 'done')
        elif active_model == 'mrp.production':
            moves = record.move_created_ids2.filtered(lambda x:
                                                      x.state == 'done')
        lines = []
        for quant in moves.mapped('quant_ids'):
            lines.append((0, 0, {'product_id': quant.product_id.id,
                                 'lot_id': quant.lot_id.id,
                                 'package_qty': quant.pck_qty or quant.qty,
                                 'quant_id': quant.id,
                                 'quant_qty': quant.qty,
                                 'ul_id': quant.ul_id.id}))
        return lines

    print_label_lines = fields.One2many(
        comodel_name='stock.print.label.line', inverse_name='wiz_id',
        string='Lines', default=_default_lines)

    @api.multi
    def print_label(self):
        for line in self.print_label_lines:
            line.quant_id.sudo().write({
                'pck_qty': line.package_qty,
                'ul_id': line.ul_id.id
                })
        return self.env['report'].get_action(
            self.mapped('print_label_lines.quant_id'),
            'stock_label_print.quant_label_report')
