# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models, api
from odoo.addons import decimal_precision as dp


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.multi
    @api.depends('product_uom_qty', 'location_id', 'location_id.usage')
    def _compute_current_date(self):
        for move in self.filtered(
                lambda x: x.product_uom_qty and x.location_id):
            out_amount = (
                move.product_uom_qty * -1 if move.location_id.usage ==
                'internal' else 0)
            in_amount = (
                move.product_uom_qty if move.location_id.usage !=
                'internal' else 0)
            move.out_amount = out_amount
            move.in_amount = in_amount
            move.in_out_amount = in_amount + out_amount

    in_amount = fields.Float(
        string='Entry', compute='_compute_current_date',
        digits=dp.get_precision('Product Unit of Measure'), store=True,
        compute_sudo=True)
    out_amount = fields.Float(
        string='Out', compute='_compute_current_date',
        digits=dp.get_precision('Product Unit of Measure'), store=True,
        compute_sudo=True)
    in_out_amount = fields.Float(
        string='Quantity', compute='_compute_current_date',
        digits=dp.get_precision('Product Unit of Measure'), store=True,
        compute_sudo=True)
