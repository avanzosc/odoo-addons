# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api, _
from odoo.tools.float_utils import float_compare, float_is_zero
from odoo.exceptions import UserError


class StockMove(models.Model):
    _inherit = 'stock.move'

    is_locked = fields.Boolean(
        related='picking_id.is_locked')
    move_type = fields.Selection(
        related='picking_id.move_type')
    picking_state = fields.Selection(
        related='picking_id.state', string="Picking State")
    show_mark_as_todo = fields.Boolean(
        related='picking_id.show_mark_as_todo')
    show_check_availability = fields.Boolean(
        compute='_compute_show_check_availability', store=True)

    @api.multi
    @api.depends('state', 'picking_id', 'picking_id.is_locked',
                 'picking_id.state')
    def _compute_show_check_availability(self):
        for move in self:
            if (not move.picking_id or move.state not in
                    ('waiting', 'confirmed', 'partially_available')):
                move.show_check_availability = False
            else:
                move.show_check_availability = (
                    move.picking_id.is_locked and move.picking_id.state in
                    ('confirmed', 'waiting', 'assigned'))

    def stock_usability_action_confirm(self):
        if self.state == 'draft':
            self._action_confirm()
            if (self.picking_id and self.picking_id.location_id.usage in
                ('supplier', 'inventory', 'production') and
                    self.picking_id.state == 'confirmed'):
                self._action_assign()

    def stock_usability_action_assign(self):
        return self._action_assign()

    def stock_usability_do_unreserve(self):
        return self._do_unreserve()

    def stock_usability_button_validate(self):
        precision_digits = self.env['decimal.precision'].precision_get(
            'Product Unit of Measure')
        for move in self:
            if move.quantity_done == 0:
                move.quantity_done = (
                    move.reserved_availability if move.picking_type_id.code ==
                    'outgoing' else move.product_uom_qty)
            no_quantities_done = all(
                float_is_zero(
                    move_line.qty_done, precision_digits=precision_digits)
                for move_line in move.picking_id.move_line_ids.filtered(
                    lambda m: m.state not in ('done', 'cancel') and
                    m.product_id.id == move.product_id.id))
            no_reserved_quantities = all(
                float_is_zero(
                    move_line.product_qty,
                    precision_rounding=move_line.product_uom_id.rounding)
                for move_line in move.picking_id.move_line_ids.filtered(
                    lambda m: m.product_id.id == move.product_id.id))
            if no_reserved_quantities and no_quantities_done:
                raise UserError(
                    _('You cannot validate a transfer if no quantites are '
                      'reserved nor done. To force the transfer, switch in '
                      'edit more and encode the done quantities.'))
            if (move.picking_type_id.use_create_lots or
                    move.picking_type_id.use_existing_lots):
                lines_to_check = move.picking_id.move_line_ids.filtered(
                    lambda m: m.product_id.id == move.product_id.id)
                if not no_quantities_done:
                    lines_to_check = lines_to_check.filtered(
                        lambda line: float_compare(
                            line.qty_done, 0,
                            precision_rounding=line.product_uom_id.rounding))
                for line in lines_to_check:
                    product = line.product_id
                    if line.product_id and line.product_id.tracking != 'none':
                        if not line.lot_name and not line.lot_id:
                            raise UserError(
                                _('You need to supply a Lot/Serial number for'
                                  ' product %s.') % product.display_name)
                if any(move.picking_id.move_line_ids.filtered(
                    lambda x: not x.move_id and x.product_id.id ==
                        move.product_id.id)):
                    raise UserError(
                        _('A "move line" was found without "move"'))
                move._action_done()

    def stock_usability_action_cancel(self):
        return self._action_cancel()

    def stock_usability_action_to_draft(self):
        return self.write({'state': 'draft'})
