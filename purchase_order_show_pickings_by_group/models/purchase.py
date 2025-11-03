# Copyright 2025 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    group_picking_count = fields.Integer(
        string="Related pickings",
        compute="_compute_group_picking_count",
    )

    def _compute_group_picking_count(self):
        for record in self:
            if record.group_id:
                pickings = self.env["stock.picking"].search_count(
                    [("group_id", "=", record.group_id.id)]
                )
                record.group_picking_count = pickings
            else:
                record.group_picking_count = 0

    def action_view_picking(self):
        self.ensure_one()
        pickings = self.env["stock.picking"].search(
            [("group_id", "=", self.group_id.id)]
        )
        return self._get_action_view_picking(pickings)
