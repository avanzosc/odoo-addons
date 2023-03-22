# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _get_new_picking_values(self):
        picking_values = super(StockMove, self)._get_new_picking_values()
        partner = self.env['res.partner'].browse(
            picking_values.get('partner_id'))
        warnings = self.env['stock.picking']._find_partner_warnings(partner)
        if warnings:
            picking_values['note'] = warnings
        return picking_values
