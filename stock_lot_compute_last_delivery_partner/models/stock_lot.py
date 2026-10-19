# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockLot(models.Model):
    _inherit = "stock.lot"

    def _compute_last_delivery_partner_id(self):
        for lot in self:
            cond = [("lot_id", "=", lot.id), ("state", "=", "done")]
            line = self.env["stock.move.line"].search(cond, order="date desc", limit=1)
            if line.picking_code == "outgoing" and line.picking_id:
                lot.last_delivery_partner_id = line.picking_id.partner_id.id
            else:
                lot.last_delivery_partner_id = False
