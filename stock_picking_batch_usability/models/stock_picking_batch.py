# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"

    in_progress = fields.Boolean(string="Is in progress", default=False)
    is_done = fields.Boolean(string="Is done", default=False)
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

    def action_confirm(self):
        result = super().action_confirm()
        self.in_progress = True
        return result

    def action_done(self):
        result = super().action_done()
        self.is_done = True
        return result

    @api.depends("picking_ids", "picking_ids.state", "in_progress", "is_done")
    def _compute_state(self):
        result = super()._compute_state()
        for batch in self:
            if batch.in_progress is False and (batch.is_done) is False:
                batch.state = "draft"
            if batch.in_progress is True and batch.is_done is False:
                batch.state = "in_progress"
            if batch.in_progress is True and batch.is_done is True:
                batch.state = "done"
        return result
