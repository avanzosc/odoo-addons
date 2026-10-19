# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
# Copyright 2025 Eñaut Alberdi - AvanzOSC

from odoo import fields, models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    product_state_id = fields.Many2one(
        comodel_name="product.state",
        string="Product State",
        related="product_id.product_tmpl_id.product_state_id",
        store=True,
        readonly=True,
        index=True,
    )
