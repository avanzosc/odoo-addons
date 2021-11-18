# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class StockMove(models.Model):
    _inherit = 'stock.move'

    show_check_availability = fields.Boolean(
        related='picking_id.show_check_availability', store=True)
    picking_type_code = fields.Selection(
        related='picking_id.picking_type_code', store=True)
    immediate_transfer = fields.Boolean(
        related='picking_id.immediate_transfer', store=True)
    move_type = fields.Selection(related='picking_id.move_type', store=True)

    def button_action_assign(self):
        self._action_assign()

    def button_do_unreserve(self):
        self._do_unreserve()
