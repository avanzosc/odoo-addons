# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"

    num_pickings_confirmed = fields.Integer(
        string="Num. Pickings Confirmed",
        compute="_compute_num_pickings",
        store=True,
        copy=False,
    )
    num_pickings_assigned = fields.Integer(
        string="Num. Pickings Assigned",
        compute="_compute_num_pickings",
        store=True,
        copy=False,
    )

    @api.depends("picking_ids", "picking_ids.state")
    def _compute_num_pickings(self):
        for batch in self:
            num_pickings_confirmed = 0
            num_pickings_assigned = 0
            if batch.picking_ids:
                pickings = batch.picking_ids.filtered(lambda x: x.state == "confirmed")
                if pickings:
                    num_pickings_confirmed = len(pickings)
                pickings = batch.picking_ids.filtered(lambda x: x.state == "assigned")
                if pickings:
                    num_pickings_assigned = len(pickings)
            batch.num_pickings_confirmed = num_pickings_confirmed
            batch.num_pickings_assigned = num_pickings_assigned

    @api.depends("company_id", "picking_type_id", "state")
    def _compute_allowed_picking_ids(self):
        result = super()._compute_allowed_picking_ids()
        for batch in self:
            allowed_pickings = batch.allowed_picking_ids
            domain = [("state", "=", "done")]
            if batch.picking_type_id:
                domain += [("picking_type_id", "=", batch.picking_type_id.id)]
            new_pickings = self.env["stock.picking"].search(domain)
            allowed_pickings += new_pickings
            batch.allowed_picking_ids = allowed_pickings
        return result
