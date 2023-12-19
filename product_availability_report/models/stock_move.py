# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models, api
from odoo.addons import decimal_precision as dp


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.multi
    def _compute_current_date(self):
        today = fields.Datetime.from_string(fields.Datetime.now())
        for move in self:
            new_fec = False
            last_date = (fields.Datetime.from_string(
                move.last_display_date) if move.last_display_date else False)
            if (not last_date or today.day != last_date.day or
                today.month != last_date.month or
                today.year != last_date.year or
                today.hour != last_date.hour or
                    today.minute != last_date.minute):
                new_fec = today
            if new_fec:
                move.last_display_date = new_fec
                move.current_date = new_fec
            if new_fec and move.location_id.usage:
                out_amount = (move.product_uom_qty * -1 if
                              move.location_id.usage == 'internal' else 0)
                entry_amount = (move.product_uom_qty if
                                move.location_id.usage != 'internal' else 0)
                move.entry_amount = entry_amount if entry_amount else 0
                move.out_amount = out_amount if out_amount else 0
                move.expected_amount = (
                    entry_amount if entry_amount else out_amount)
                if move.location_id.usage == 'internal':
                    move.reserved_availability_amount = (
                        move.reserved_availability)

    last_display_date = fields.Datetime(
        string='last_display_date', compute='_compute_current_date',
        store=True, compute_sudo=True)
    current_date = fields.Datetime(
        string='Current date', compute='_compute_current_date',
        compute_sudo=True)
    product_tmpl_id = fields.Many2one(
        string='Product template', related='product_id.product_tmpl_id',
        comodel_name='product.template', store=True, compute_sudo=True)
    picking_origin = fields.Char(
        string='Picking origin', related='picking_id.origin',
        store=True, compute_sudo=True)
    entry_amount = fields.Float(
        string='Entry', compute='_compute_current_date',
        digits=dp.get_precision('Product Unit of Measure'), store=True,
        compute_sudo=True)
    out_amount = fields.Float(
        string='Out', compute='_compute_current_date',
        digits=dp.get_precision('Product Unit of Measure'), store=True,
        compute_sudo=True)
    expected_amount = fields.Float(
        string='Expected', compute='_compute_current_date',
        digits=dp.get_precision('Product Unit of Measure'), store=True,
        compute_sudo=True)
    reserved_availability_amount = fields.Float(
        string='Reserved', compute='_compute_current_date',
        digits=dp.get_precision('Product Unit of Measure'), store=True,
        compute_sudo=True)
