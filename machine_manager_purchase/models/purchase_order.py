# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    machine_ids = fields.One2many(
        string="Machines",
        comodel_name="machine",
        inverse_name="purchase_id",
    )
    machine_count = fields.Integer(
        compute="_compute_machine_count",
    )

    @api.depends("machine_ids")
    def _compute_machine_count(self):
        for order in self:
            order.machine_count = len(order.machine_ids)
