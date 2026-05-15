# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    total_weight_qty = fields.Float(
        string="Total Weight", compute="_compute_total_weight_qty", store=True
    )
    weight_uom_name = fields.Char(
        string="Weight unit of measure label", related="product_id.weight_uom_name"
    )

    @api.depends("quantity", "product_id", "product_id.weight")
    def _compute_total_weight_qty(self):
        for line in self:
            line.total_weight_qty = line.quantity * (line.product_id.weight or 0)
