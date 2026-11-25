# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, models
from odoo.exceptions import UserError


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    @api.onchange("lot_id")
    def _onchange_lot_id_zero_qty(self):
        for line in self:
            if (
                not line.lot_id
                and line.product_id.tracking != "none"
                and line.picking_id.state == "done"
            ):
                line.qty_done = 0

    @api.onchange("qty_done")
    def _onchange_qty_done_require_lot(self):
        for line in self:
            if (
                line.qty_done > 0
                and not line.lot_id
                and line.product_id.tracking != "none"
                and line.picking_id.state == "done"
            ):
                line.qty_done = 0
                raise UserError(
                    _(
                        "You must set a lot/serial number on line '%s' before"
                        " changing the quantity."
                    )
                    % line.product_id.display_name
                )
