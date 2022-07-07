# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    location_change_id = fields.Many2one(
        string="Location Change",
        comodel_name="stock.location",
        related="batch_id.location_change_id",
        store=True)
