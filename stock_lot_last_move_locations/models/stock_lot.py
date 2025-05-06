# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockLot(models.Model):
    _inherit = "stock.lot"

    last_move_locations = fields.Char(copy=False)
