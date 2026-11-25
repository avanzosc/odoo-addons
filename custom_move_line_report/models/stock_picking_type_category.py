# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models
from odoo.modules.module import get_module_path

if not get_module_path("stock_picking_type_category", display_warning=False):

    class StockPickingTypeCategory(models.Model):
        _name = "stock.picking.type.category"
        _description = "Stock Picking Type Category"

        name = fields.Char()
