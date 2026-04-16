# Copyright 2023 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    group_detailed_operations_visible = fields.Boolean(
        string="Detailed Operations Always Visible in Pickings",
        implied_group="stock_picking_usability.group_detailed_operations_visible",
    )
