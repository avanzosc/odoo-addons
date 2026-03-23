# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    machine_ids = fields.One2many(
        string="Machines",
        comodel_name="machine",
        inverse_name="in_picking_id",
    )
    machine_count = fields.Integer(
        compute="_compute_machine_count",
    )

    @api.depends("machine_ids")
    def _compute_machine_count(self):
        for picking in self:
            picking.machine_count = len(picking.machine_ids)
