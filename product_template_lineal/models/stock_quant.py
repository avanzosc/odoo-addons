# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    lineal_id = fields.Many2one(
        string="Lineal",
        comodel_name="product.lineal",
        related="product_id.lineal_id",
        store=True,
    )
