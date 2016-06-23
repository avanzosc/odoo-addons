# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class WizDeleteSaleLine(models.TransientModel):
    _name = 'wiz.delete.sale.line'

    lines = fields.One2many(
        comodel_name='wiz.delete.sale.line.line',
        inverse_name='wiz_id', string='Sale lines')

    @api.model
    def default_get(self, var_fields):
        sale_obj = self.env['sale.order']
        vals = []
        for sale in sale_obj.browse(self.env.context.get('active_ids')):
            for line in sale.order_line:
                line_vals = {'delete_record': False,
                             'sale_line': line.id,
                             'name': line.name,
                             'product_uom_qty': line.product_uom_qty,
                             'price_unit': line.price_unit,
                             'price_subtotal': line.price_subtotal}
                vals.append(line_vals)
        return {'lines': vals}

    @api.multi
    def button_delete_sale_lines(self):
        self.ensure_one()
        for wiz in self:
            lines = wiz.lines.filtered(lambda x: x.delete_record)
            for line in lines:
                line.sale_line.unlink()


class WizDeleteSaleLineLine(models.TransientModel):
    _name = 'wiz.delete.sale.line.line'

    wiz_id = fields.Many2one(
        comodel_name='wiz.delete.sale.line', string='Wizard')
    delete_record = fields.Boolean(string='delete')
    sale_line = fields.Many2one('sale.order.line', string='Sale line')
    name = fields.Char('Description', readonly=True)
    product_uom_qty = fields.Float(
        'Quantity', digits=dp.get_precision('Product UoS'), readonly=True)
    price_unit = fields.Float(
        'Unit Price', digits=dp.get_precision('Product Price'), readonly=True)
    price_subtotal = fields.Float(
        'Subtotal', digits=dp.get_precision('Account'), readonly=True)
