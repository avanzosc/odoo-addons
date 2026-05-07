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
                record.group_picking_count = self.env["stock.picking"].search_count(
                    [("group_id", "=", record.group_id.id)]
                )
            else:
                record.group_picking_count = 0

    def action_view_group_picking(self):
        self.ensure_one()
        pickings = (
            self.env["stock.picking"].search([("group_id", "=", self.group_id.id)])
            if self.group_id
            else self.picking_ids
        )
        result = self.env["ir.actions.actions"]._for_xml_id(
            "stock.action_picking_tree_all"
        )
        result["context"] = {}
        result["domain"] = [("id", "in", pickings.ids)]
        return result
