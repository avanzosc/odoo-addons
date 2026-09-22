# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockLot(models.Model):
    _inherit = "stock.lot"

    state = fields.Selection(
        [
            ("new", "New"),
            ("active", "Active"),
            ("inactive", "Inactive"),
            ("finished", "Finished"),
        ],
        default="new",
        copy=False,
    )
