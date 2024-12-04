# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    packaging_units = fields.Float(
        string="Packaging Units",
        related="lot_id.packaging_units",
        store=True,
        copy=False,
    )
