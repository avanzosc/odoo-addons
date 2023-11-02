# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    egg = fields.Boolean(
        string="Egg",
        related="product_id.egg",
        store=True)
    batch_location_id = fields.Many2one(
        string="Mother Location",
        comodel_name="stock.location",
        related="batch_id.location_id",
        store=True)
    batch_category_type_id = fields.Many2one(
        string="Batch Section",
        comodel_name="category.type",
        related="batch_location_id.type_id",
        store=True)
