# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    purchase_line_confirmation_date = fields.Date(
        related="purchase_line_id.confirmation_date", store=True, copy=False
    )
