# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"

    @api.depends("company_id", "picking_type_id", "state")
    def _compute_allowed_picking_ids(self):
        result = super()._compute_allowed_picking_ids()
        for batch in self:
            domain = [
                ("company_id", "=", batch.company_id.id),
                ("state", "=", "done"),
            ]
            if batch.picking_type_id:
                domain.append(("picking_type_id", "=", batch.picking_type_id.id))
            done_pickings = self.env["stock.picking"].search(
                domain, order="date_done desc", limit=1000
            )
            batch.allowed_picking_ids |= done_pickings
        return result
