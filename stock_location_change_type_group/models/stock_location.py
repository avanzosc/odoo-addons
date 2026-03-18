# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockLocation(models.Model):
    _inherit = "stock.location"

    user_has_group_change_type = fields.Boolean(
        compute="_compute_user_has_group_change_type"
    )

    @api.depends_context("uid")
    def _compute_user_has_group_change_type(self):
        user_has_group = self.env.user.has_group(
            "stock_location_change_type_group.group_stock_location_change_type"
        )
        for location in self:
            location.user_has_group_change_type = user_has_group
