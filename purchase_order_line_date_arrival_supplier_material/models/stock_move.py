# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    date_arrival_supplier_material = fields.Date(
        related="purchase_line_id.date_arrival_supplier_material",
        copy=False,
        store=True,
        readonly=False,
    )
