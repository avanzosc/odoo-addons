# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    prefill_quantity = fields.Boolean(
        default=True,
        help="When a move of this operation type is reserved against a "
        "location that doesn't hold real stock (e.g. a vendor location "
        "on a receipt), Odoo has no real quantity to reserve and fills "
        "the quantity with the full amount demanded, so it shows as "
        "already done. Uncheck this to leave the quantity at 0 instead, "
        "so it has to be entered manually with what was actually done.",
    )
