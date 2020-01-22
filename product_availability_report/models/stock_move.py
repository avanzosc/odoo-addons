# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models, api
from odoo.addons import decimal_precision as dp


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.multi
    @api.depends('product_uom_qty')
    def _compute_entry_out_expected_amount(self):
        for move in self.filtered(
                lambda x: x.product_uom_qty and x.location_id and
                x.location_id.usage):
            out_amount = (move.product_uom_qty * -1 if
                          move.location_id.usage == 'internal' else 0)
            entry_amount = (move.product_uom_qty if
                            move.location_id.usage != 'internal' else 0)
            move.entry_amount = entry_amount if entry_amount else 0
            move.out_amount = out_amount if out_amount else 0
            move.expected_amount = entry_amount if entry_amount else out_amount

    @api.multi
    @api.depends('entry_amount', 'out_amount', 'expected_amount',
                 'product_uom_qty', 'move_line_ids',
                 'move_line_ids.product_qty')
    def _compute_reserved_availability_amount(self):
        line_obj = self.env['stock.move.line']
        result = {data['move_id'][0]:
                  data['product_qty'] for data in line_obj.read_group(
                      [('move_id', 'in', self.ids)],
                      ['move_id', 'product_qty'], ['move_id'])}
        for move in self.filtered(
                lambda x: x.location_id and x.location_id.usage and
                x.location_id.usage == 'internal'):
            move.reserved_availability_amount = (
                move.product_id.uom_id._compute_quantity(
                    result.get(move.id, 0.0), move.product_uom,
                    rounding_method='HALF-UP'))

    product_tmpl_id = fields.Many2one(
        string='Product template', related='product_id.product_tmpl_id',
        comodel_name='product.template', store=True)
    picking_origin = fields.Char(
        string='Picking origin', related='picking_id.origin',
        store=True)
    entry_amount = fields.Float(
        string='Entry', compute='_compute_entry_out_expected_amount',
        digits=dp.get_precision('Product Unit of Measure'), store=True)
    out_amount = fields.Float(
        string='Out', compute='_compute_entry_out_expected_amount',
        digits=dp.get_precision('Product Unit of Measure'), store=True)
    expected_amount = fields.Float(
        string='Expected', compute='_compute_entry_out_expected_amount',
        digits=dp.get_precision('Product Unit of Measure'), store=True)
    reserved_availability_amount = fields.Float(
        string='Reserved', compute='_compute_reserved_availability_amount',
        digits=dp.get_precision('Product Unit of Measure'), store=True)
