# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    readonly_technical_info = fields.Boolean(
        string="Read Only Technical Information",
        compute="_compute_readonly_technical_info",
    )

    def _compute_readonly_technical_info(self):
        for warehouse in self:
            has_group = self.env.user.has_group(
                "stock_warehouse_editor.group_warehouse_editor"
            )
            warehouse.readonly_technical_info = not has_group
