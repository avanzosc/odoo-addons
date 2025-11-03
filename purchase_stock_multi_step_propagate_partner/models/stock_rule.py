# Copyright 2025 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class StockRule(models.Model):
    _inherit = "stock.rule"

    def _push_prepare_move_copy_values(self, move_to_copy, new_date):
        new_move_vals = super()._push_prepare_move_copy_values(move_to_copy, new_date)
        if "partner_id" not in new_move_vals:
            new_move_vals["partner_id"] = (
                move_to_copy.partner_id.id or move_to_copy.picking_id.partner_id.id
            )
        return new_move_vals
